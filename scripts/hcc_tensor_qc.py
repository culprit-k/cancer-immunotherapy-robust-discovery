#!/usr/bin/env python3
"""Full local tensor QC for HCC multichannel TIFFs and paired masks.

Run locally only. Does not upload data, infer channel order, or establish VirTues
compatibility. Requires numpy, tifffile. Outputs aggregate/per-ROI QC JSON/CSV.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path
from typing import Any
import numpy as np
import tifffile

IMG_SUFFIX={".tif",".tiff"}
MASK_SUFFIX={".tif",".tiff",".png",".npy"}

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def read_array(path: Path) -> np.ndarray:
    if path.suffix.lower()==".npy":
        return np.load(path, allow_pickle=False)
    if path.suffix.lower()==".png":
        import imageio.v3 as iio
        return iio.imread(path)
    return tifffile.imread(path)

def describe(path: Path, mask: bool=False) -> dict[str,Any]:
    try:
        a=read_array(path)
        finite=np.isfinite(a) if np.issubdtype(a.dtype,np.number) else np.zeros(a.shape,dtype=bool)
        out={"path":str(path),"sha256":sha256_file(path),"read_ok":True,
             "shape":list(a.shape),"ndim":int(a.ndim),"dtype":str(a.dtype),
             "size":int(a.size),"finite_fraction":float(finite.mean()) if a.size else 0.0,
             "min":float(np.min(a)) if a.size and finite.all() else None,
             "max":float(np.max(a)) if a.size and finite.all() else None}
        if mask:
            if a.size and finite.all():
                vals,counts=np.unique(a,return_counts=True)
                out["unique_label_count"]=int(len(vals))
                out["labels_and_counts"]=[{"label":v.item() if hasattr(v,"item") else v,"count":int(c)}
                    for v,c in zip(vals[:100],counts[:100])]
                out["labels_truncated"]=len(vals)>100
            out["is_integer_dtype"]=bool(np.issubdtype(a.dtype,np.integer))
        else:
            out["within_0_1"]=bool(a.size and finite.all() and np.min(a)>=0 and np.max(a)<=1)
            out["likely_channel_axis_candidates"]=[i for i,n in enumerate(a.shape) if n in range(10,301)]
        return out
    except Exception as e:
        return {"path":str(path),"read_ok":False,"error":f"{type(e).__name__}: {e}"}

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--images",type=Path,required=True)
    ap.add_argument("--cell-masks",type=Path,required=True)
    ap.add_argument("--stromal-masks",type=Path,required=True)
    ap.add_argument("--channel-map",type=Path,required=True)
    ap.add_argument("--outdir",type=Path,required=True)
    ap.add_argument("--channel-axis",type=int,default=None,
                    help="Optional explicit image channel axis; never inferred silently.")
    args=ap.parse_args()
    for d in (args.images,args.cell_masks,args.stromal_masks):
        if not d.is_dir(): ap.error(f"Not a directory: {d}")
    for p in (args.images,args.cell_masks,args.stromal_masks,args.channel_map):
        if not p.exists(): ap.error(f"Missing input: {p}")
    with args.channel_map.open(newline="",encoding="utf-8-sig") as f:
        channel_rows=list(csv.DictReader(f))
    required={"channel_index","marker","uniprot_id","source_label","intensity_semantics","mapping_evidence"}
    map_errors=[]
    if not channel_rows: map_errors.append("Channel map has no data rows.")
    if channel_rows and not required.issubset(channel_rows[0]):
        map_errors.append("Channel map is missing required columns: "+", ".join(sorted(required-set(channel_rows[0]))))
    indices=[]
    for i,row in enumerate(channel_rows,1):
        try: indices.append(int(row["channel_index"]))
        except Exception: map_errors.append(f"Row {i}: channel_index is not an integer.")
    if indices and sorted(indices)!=list(range(len(indices))):
        map_errors.append("channel_index values must be contiguous and zero-based.")
    if len(indices)!=len(set(indices)): map_errors.append("Duplicate channel_index values.")
    for i,row in enumerate(channel_rows,1):
        for key in ("marker","uniprot_id","source_label","intensity_semantics","mapping_evidence"):
            if key in row and not str(row[key]).strip():
                map_errors.append(f"Row {i}: empty {key}; resolve explicitly rather than guessing.")
    def by_stem(folder,suffixes):
        return {p.stem:p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in suffixes}
    images=by_stem(args.images,IMG_SUFFIX)
    cells=by_stem(args.cell_masks,MASK_SUFFIX)
    stroma=by_stem(args.stromal_masks,MASK_SUFFIX)
    names=sorted(set(images)|set(cells)|set(stroma))
    rows=[]; errors=[]; warnings=[]
    if not names: errors.append("No image/mask files found.")
    for name in names:
        row={"roi_stem":name,"has_image":name in images,"has_cell_mask":name in cells,"has_stromal_mask":name in stroma}
        if name not in images or name not in cells or name not in stroma:
            row["roi_status"]="BLOCKED_MISSING_TRIPLET"; rows.append(row); errors.append(f"{name}: incomplete image/cell/stromal triplet"); continue
        im=describe(images[name]); cm=describe(cells[name],True); sm=describe(stroma[name],True)
        row.update({"image":im,"cell_mask":cm,"stromal_mask":sm})
        local=[]
        if not im.get("read_ok"): local.append("image_read_failed")
        if not cm.get("read_ok"): local.append("cell_mask_read_failed")
        if not sm.get("read_ok"): local.append("stromal_mask_read_failed")
        if im.get("read_ok") and args.channel_axis is not None:
            axis=args.channel_axis if args.channel_axis>=0 else len(im["shape"])+args.channel_axis
            if axis<0 or axis>=len(im["shape"]): local.append("channel_axis_out_of_range")
            else:
                row["declared_channel_axis"]=axis
                row["observed_channel_count"]=im["shape"][axis]
                if channel_rows and im["shape"][axis]!=len(channel_rows): local.append("channel_map_count_mismatch")
        if im.get("read_ok") and cm.get("read_ok") and tuple(im["shape"][-2:])!=tuple(cm["shape"][-2:]):
            warnings.append(f"{name}: trailing image dimensions {im['shape'][-2:]} differ from cell-mask shape {cm['shape']}")
            local.append("image_cell_mask_shape_needs_axis_review")
        if cm.get("read_ok") and sm.get("read_ok") and cm["shape"]!=sm["shape"]:
            local.append("cell_stromal_mask_shape_mismatch")
        for label,obj in (("image",im),("cell_mask",cm),("stromal_mask",sm)):
            if obj.get("read_ok") and obj.get("finite_fraction")!=1.0: local.append(label+"_nonfinite_values")
        if cm.get("read_ok") and not cm.get("is_integer_dtype"): local.append("cell_mask_noninteger_dtype")
        if sm.get("read_ok") and not sm.get("is_integer_dtype"): local.append("stromal_mask_noninteger_dtype")
        row["flags"]=sorted(set(local))
        row["roi_status"]="PASS_TENSOR_QC_PRELIMINARY" if not local else "REVIEW_REQUIRED"
        rows.append(row)
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"hcc_tensor_qc.json").write_text(json.dumps({
      "status":"PASS_METADATA_AND_BASIC_TENSOR_CHECKS" if not errors and not map_errors and all(r.get("roi_status")=="PASS_TENSOR_QC_PRELIMINARY" for r in rows) else "BLOCKED_OR_REVIEW_REQUIRED",
      "scope":"Private local QC only. Shape agreement and a clean report do not prove spatial alignment, correct channel semantics, preprocessing equivalence or VirTues compatibility.",
      "roi_count_union":len(names),"image_count":len(images),"cell_mask_count":len(cells),"stromal_mask_count":len(stroma),
      "complete_triplets":sum(r.get("has_image") and r.get("has_cell_mask") and r.get("has_stromal_mask") for r in rows),
      "channel_map_rows":len(channel_rows),"channel_map_errors":map_errors,"errors":errors,"warnings":warnings,"rois":rows
    },indent=2,default=str),encoding="utf-8")
    with (args.outdir/"hcc_tensor_qc_summary.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["roi_stem","roi_status","has_image","has_cell_mask","has_stromal_mask","flags"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows: w.writerow({k:json.dumps(r.get(k)) if k=="flags" else r.get(k) for k in fields})
    print(json.dumps({"status":"BLOCKED_OR_REVIEW_REQUIRED" if errors or map_errors or any(r.get("roi_status")!="PASS_TENSOR_QC_PRELIMINARY" for r in rows) else "PASS_METADATA_AND_BASIC_TENSOR_CHECKS","roi_count_union":len(names),"complete_triplets":sum(r.get("has_image") and r.get("has_cell_mask") and r.get("has_stromal_mask") for r in rows),"channel_map_rows":len(channel_rows),"map_errors":map_errors,"errors":errors,"warnings":warnings},indent=2))
    return 2 if errors or map_errors or any(r.get("roi_status")!="PASS_TENSOR_QC_PRELIMINARY" for r in rows) else 0

if __name__=="__main__": raise SystemExit(main())
