import pytest
from graph_filter import *


def test_rules_invalid_json_string():
    invalid_rules_str = "Not a valid JSON string!"
    with pytest.raises(json.JSONDecodeError):
        parse_rules(invalid_rules_str)

def test_two_rules_not_in_a_list():
    invalid_rules = '{"type": "min", "count": 2, "sum": 7}, {"type": "max", "count": 1, "sum": 8}'
    with pytest.raises(json.JSONDecodeError):
        parse_rules(invalid_rules)

def test_rules_invalid_json_object():
    invalid_rules = '"type": "max", "count": 3, "sum": 6'
    with pytest.raises(json.JSONDecodeError):
        parse_rules(invalid_rules)

def test_rules_incomplete():
    invalid_rules_str = '{"type": "min", "count": 8}'
    invalid_rules = parse_rules(invalid_rules_str)
    with pytest.raises(ValueError, match = "Rule is incomplete or has incorrect keys"):
        validate_rules(invalid_rules)

def test_rules_incorrect_keys():
    invalid_rules_str = '{"sort": "exact", "number": 4, "total": 7}'
    invalid_rules = parse_rules(invalid_rules_str)
    with pytest.raises(ValueError, match = "Rule is incomplete or has incorrect keys"):
        validate_rules(invalid_rules)

def test_rules_incorrect_values():
    invalid_rules_str = '{"type": 1, "count": "three", "sum": False}'
    invalid_rules = parse_rules(invalid_rules_str)
    with pytest.raises(ValueError, match = "Rule has incorrect values"):
        validate_rules(invalid_rules)

def test_rules_wrong_type():
    invalid_rules_str = '{"type": "exactly", "count": 2, "sum": 6}'
    invalid_rules = parse_rules(invalid_rules_str)
    with pytest.raises(ValueError, match = "Wrong rule type provided"):
        validate_rules(invalid_rules)