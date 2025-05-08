import random
from graph_filter.filter_util import *


def generate_filename(tmp_path, test_name):
    return tmp_path / f"history_test_{test_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"



def test_save_history_file_created(tmp_path):
    filename = generate_filename(tmp_path, "file_created")
    rules = [{"type": "max", "count": 4, "sum": 6}]
    passed_graphs = ["D?{", "DBc", "Dh_", "D@{", "Dx_", "DJc", "DbW", "Dhc", "DjW", "Db[", "D`{", "Dlc"]
    save_history(rules, 13, 12, passed_graphs, str(filename))
    assert filename.exists()


def test_save_history_writes_correct_data_exact_rule(tmp_path):
    filename = generate_filename(tmp_path, "writes_correct_data_exact_rule")
    rules = [{"type": "exact", "count": 1, "sum": 7}]
    passed_graphs = ["ILwG@wHQO", "IEEm{?LyG", "IPGO?_?G?", "I`HKPKGg?", "ICDTGANhw"]
    save_history(rules, 9, 5, passed_graphs, str(filename))

    content = filename.read_text().strip()
    fields = content.split("\t")
    assert len(fields) == 5

    assert json.dumps(rules) == fields[3]
    assert "9" == fields[1]
    assert "5" == fields[2]

    written_passed_graphs = eval(fields[4])
    assert written_passed_graphs == passed_graphs


def test_save_history_writes_correct_data_combination_of_rules(tmp_path):
    filename = generate_filename(tmp_path, "writes_correct_data_combination_of_rules")
    rules = [{"type": "min", "count": 2, "sum": 3}, {"type": "max", "count": 1, "sum": 5}]
    passed_graphs = ["I?S?_?KK?", "I???_AOD?", "IGGCa@??G", "ID???SQ@_", "I?HA_C@??]"]
    save_history(rules, 6, 5, passed_graphs, str(filename))

    content = filename.read_text().strip()
    fields = content.split("\t")
    assert len(fields) == 5

    assert json.dumps(rules) == fields[3]
    assert "6" == fields[1]
    assert "5" == fields[2]

    written_passed_graphs = eval(fields[4])
    assert written_passed_graphs == passed_graphs


def test_save_history_full_verification(tmp_path):
    filename = generate_filename(tmp_path, "full_verification")
    rules = [{"type": "min", "count": 1, "sum": 4}]
    passed_graphs = ["D?{", "DBc", "Dh_", "D@{", "Dx_", "DJc", "DbW", "Dhc", "DjW", "Db[", "D`{", "Dlc"]
    random_graph_from_passed_graphs = random.choice(passed_graphs)

    save_history(rules, 21, 12, passed_graphs, str(filename))

    content = filename.read_text().strip()
    fields = content.split("\t")
    timestamp, input_number, output_number, filter_string, passed_graphs_str = fields

    timestamp_str_from_filename = filename.name.removeprefix("history_test_full_verification_").removesuffix(".log")

    def assert_timestamps_are_close(ts1: str, ts2: str, tolerance_sec = 5):
        dt1 = datetime.strptime(ts1, "%Y-%m-%d_%H-%M-%S")
        dt2 = datetime.strptime(ts2, "%Y-%m-%d_%H-%M-%S")
        assert (abs(dt1 - dt2)).total_seconds() <= tolerance_sec

    assert_timestamps_are_close(timestamp, timestamp_str_from_filename)

    assert int(input_number) == 21
    assert int(output_number) == 12
    assert json.loads(filter_string) == [{"type": "min", "count": 1, "sum": 4}]
    assert random_graph_from_passed_graphs in passed_graphs_str