import pytest

from analysis.panel_metadata_qc import audit_panel_structure


FIELDS = ["Channel", "MetalTag", "Target"]


def test_panel_structure_passes_clean_contiguous_panel():
    rows = [
        {"Channel": "1", "MetalTag": "113Cd", "Target": "CD3"},
        {"Channel": "2", "MetalTag": "115In", "Target": "CD8"},
        {"Channel": "3", "MetalTag": "141Pr", "Target": "PD1"},
    ]
    result = audit_panel_structure(FIELDS, rows)
    assert result["structural_qc_pass"] is True
    assert result["channels_numeric_and_contiguous_from_1"] is True
    assert result["missing_required_columns"] == []


@pytest.mark.parametrize(
    "fields,rows",
    [
        (["Channel", "Target"], [{"Channel": "1", "Target": "CD3"}]),
        (FIELDS, [{"Channel": "1", "MetalTag": "", "Target": "CD3"}]),
        (FIELDS, [
            {"Channel": "1", "MetalTag": "113Cd", "Target": "CD3"},
            {"Channel": "1", "MetalTag": "115In", "Target": "CD8"},
        ]),
        (FIELDS, [
            {"Channel": "1", "MetalTag": "113Cd", "Target": "CD3"},
            {"Channel": "2", "MetalTag": "113Cd", "Target": "CD8"},
        ]),
        (FIELDS, [
            {"Channel": "1", "MetalTag": "113Cd", "Target": "CD3"},
            {"Channel": "2", "MetalTag": "115In", "Target": "CD3"},
        ]),
        (FIELDS, [
            {"Channel": "1", "MetalTag": "113Cd", "Target": "CD3"},
            {"Channel": "3", "MetalTag": "115In", "Target": "CD8"},
        ]),
    ],
)
def test_panel_structure_fails_invalid_panels(fields, rows):
    assert audit_panel_structure(fields, rows)["structural_qc_pass"] is False


def test_panel_structure_is_case_insensitive_for_duplicate_detection():
    rows = [
        {"Channel": "1", "MetalTag": "113Cd", "Target": "CD3"},
        {"Channel": "2", "MetalTag": "115In", "Target": "cd3"},
    ]
    result = audit_panel_structure(FIELDS, rows)
    assert result["duplicate_target_values"] == ["cd3"]
    assert result["structural_qc_pass"] is False
