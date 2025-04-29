import subprocess


def test_run_filter_no_arguments():
    result = subprocess.run(
        ["bash", "../run_filter.sh"],
        capture_output = True,
        text = True
    )
    assert result.returncode == 1
    assert "Usage: ./run_filter.sh <number_of_vertices> <rules_json>" in result.stderr


def test_run_filter_only_vertices():
    result = subprocess.run(
        ["bash", "../run_filter.sh", "5"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Usage: ./run_filter.sh <number_of_vertices> <rules_json>" in result.stderr

def test_run_filter_only_rules():
    result = subprocess.run(
        ["bash", "../run_filter.sh", '{"type": "exact", "count": 1, "sum": 1}'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Usage: ./run_filter.sh <number_of_vertices> <rules_json>" in result.stderr


def test_run_filter_invalid_number_of_vertices():
    result = subprocess.run(
        ["bash", "../run_filter.sh", "five", '{"type": "exact", "count": 1, "sum": 1}'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Error: number_of_vertices must be a positive integer." in result.stderr