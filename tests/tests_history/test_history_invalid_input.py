import pytest
from graph_filter.filter_util import *


def generate_filename(tmp_path, test_name):
    return tmp_path / f"history_test_{test_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"



def test_save_history_invalid_rules(tmp_path):
    filename = generate_filename(tmp_path, "invalid_rules")
    invalid_rules = "Invalid rules"
    passed_graphs = ["graph1", "graph2"]

    with pytest.raises(TypeError, match = "Rules must be a list or a dict."):
        save_history(invalid_rules, 3, 2, passed_graphs, str(filename))


def test_save_history_invalid_input_output_count(tmp_path):
    filename = generate_filename(tmp_path, "invalid_input_output_count")
    rules = {"type": "max", "count": 11, "sum": 19}
    passed_graphs = ["DJ?", "DOk", "DOG", "Dgw", "D??"]

    with pytest.raises(TypeError, match = "Input count and output count must be integers."):
        save_history(rules, "six", "five", passed_graphs, str(filename))


def test_save_history_invalid_passed_graphs(tmp_path):
    filename = generate_filename(tmp_path, "invalid_passed_graphs")
    rules = {"type": "max", "count": 11, "sum": 19}
    invalid_passed_graphs = {"DJ?", "DOk", "DOG", "Dgw", "D??"}

    with pytest.raises(TypeError, match = "Passed graphs must be a list."):
        save_history(rules, 6, 5, invalid_passed_graphs, str(filename))


def test_save_history_invalid_filename(tmp_path):
    filename = None
    rules = {"type": "max", "count": 11, "sum": 19}
    passed_graphs = ["DJ?", "DOk", "DOG", "Dgw", "D??"]

    with pytest.raises(TypeError, match = "History filename must be a string."):
        save_history(rules, 6, 5, passed_graphs, filename)



def test_save_history_output_greater_than_input(tmp_path):
    filename = generate_filename(tmp_path, "output_greater_than_input")
    rules = {"type": "max", "count": 11, "sum": 19}
    invalid_passed_graphs = ["DJ?", "DOk", "DOG", "Dgw", "D??"]

    with pytest.raises(ValueError, match = "Output count must be less than or equal to input count."):
        save_history(rules, 4, 5, invalid_passed_graphs, str(filename))


def test_save_history_passed_graphs_mismatch(tmp_path):
    filename = generate_filename(tmp_path, "passed_graphs_mismatch")
    rules = {"type": "max", "count": 11, "sum": 19}
    passed_graphs = ["DJ?", "DOk", "DOG", "Dgw", "D??"]

    with pytest.raises(ValueError, match = "The number of passed graphs must be less than or equal to output count."):
        save_history(rules, 10, 4, passed_graphs, str(filename))