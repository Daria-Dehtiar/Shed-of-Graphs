import pytest
import io
from graph_filter.filter_main import *



def make_history_file(tmp_path):
    return str(tmp_path / "dummy_history.log")


def test_filter_no_rules(monkeypatch, capsys, tmp_path):
    history_file = make_history_file(tmp_path)

    monkeypatch.setattr(sys, "argv", ["filter_main.py", history_file])

    with pytest.raises(SystemExit) as error:
        main()
    captured = capsys.readouterr()

    assert "Usage: python filter_main.py <rules_json>" in captured.err
    assert error.value.code == 1


def test_filter_no_graphs(monkeypatch, capsys, tmp_path):
    history_file = make_history_file(tmp_path)

    monkeypatch.setattr(sys, "argv", ["filter_main.py", '{"type": "exact", "count": 1, "sum": 1}', history_file])
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))

    input_count, output_count, passed_graphs, = main()
    captured = capsys.readouterr()

    assert captured.out.strip() == ""
    assert captured.err.strip() == ""
    assert input_count == 0
    assert output_count == 0
    assert passed_graphs == []


def test_filter_invalid_graph_(monkeypatch, capsys, tmp_path):
    history_file = make_history_file(tmp_path)
    rules = '{"type": "exact", "count": 1, "sum": 1}'

    monkeypatch.setattr(sys, 'argv', ['filter_main.py', rules, history_file])

    invalid_graph_input = io.StringIO("this_is_not_a_valid_graph\n")
    monkeypatch.setattr(sys, 'stdin', invalid_graph_input)

    input_count, output_count, passed_graphs = main()
    captured = capsys.readouterr()

    assert "Error parsing graph" in captured.err
    assert captured.out.strip() == ""
    assert input_count == 1
    assert output_count == 0
    assert passed_graphs == []