import pytest
from graph_filter import *


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

    with pytest.raises(TypeError, match = "Rules must be a list or a dict."):
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


def test_save_history_passed_graphs_more_than_20(tmp_path):
    filename = generate_filename(tmp_path, "passed_graphs_more_than_20")
    rules = {"type": "max", "count": 11, "sum": 19}
    invalid_passed_graphs = ["graf1", "graf2", "graf3", "graf4", "graf5", "graf6", "graf7", "graf8", "graf9", "graf10",
                             "graf11", "graf12", "graf13", "graf14", "graf15", "graf16", "graf17", "graf18", "graf19",
                             "graf20", "graf21", "graf22", "graf23", "graf24"]

    with pytest.raises(ValueError, match = "The number of recently passed graphs must be less than or equal to 20."):
        save_history(rules, 25, 24, invalid_passed_graphs, str(filename))


def test_save_history_passed_graphs_mismatch(tmp_path):
    filename = generate_filename(tmp_path, "passed_graphs_mismatch")
    rules = {"type": "max", "count": 11, "sum": 19}
    invalid_passed_graphs = ["DJ?", "DOk", "DOG", "Dgw", "D??"]

    with pytest.raises(ValueError, match = "The number of recently passed graphs must be equal to output count if fewer "
                                           "than 20."):
        save_history(rules, 10, 6, invalid_passed_graphs, str(filename))