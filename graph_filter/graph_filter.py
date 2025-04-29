import json
import sys
from datetime import datetime

import networkx as nx


def parse_rules(rules_str):
    try:
        rules = json.loads(rules_str)
        if isinstance(rules, dict):
            return [rules]
        return rules
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON filter: {e}", file=sys.stderr)
        sys.exit(1)


def validate_rules(rules):
    for rule in rules:
        if "type" not in rule or "count" not in rule or "sum" not in rule:
            raise ValueError(f'Rule is incomplete or has incorrect keys: {rule}\n'
                             f'Each rule must contain "type", "count" and "sum".' )

        if not isinstance(rule["type"], str) or not isinstance(rule["count"], int) or not isinstance(rule["sum"], int):
            raise ValueError(f'Rule has incorrect values: {rule}\n'
                             f'Type: {rule["type"]} must be a string, count: {rule["count"]} must be an integer, '
                             f'sum: {rule["sum"]} must be an integer.')

        if rule["type"] not in {"min", "max", "exact"}:
            raise ValueError(f'Wrong rule type provided: {rule["type"]}\n'
                             f'Type: {rule["type"]} must be one of "min", "max" or "exact".')


def edges_with_degree_sum(graph, target_sum):
    degrees = dict(graph.degree())

    return [
        (u, v) for u, v in graph.edges()
        if degrees[u] + degrees[v] == target_sum
    ]


def passes_all_rules(graph, rules):
    for rule in rules:
        edges = edges_with_degree_sum(graph, rule["sum"])
        count = len(edges)

        if rule["type"] == "exact" and count != rule["count"]:
            return False
        if rule["type"] == "min" and count <= rule["count"]:
            return False
        if rule["type"] == "max" and count >= rule["count"]:
            return False
    return True


def save_history(rules, input_count, output_count, passed_graphs, history_filename):
    if not isinstance(rules, (list, dict)):
        raise TypeError("Rules must be a list or a dict.")
    if not isinstance(input_count, int) or not isinstance(output_count, int):
        raise TypeError("Input count and output count must be integers.")
    if not isinstance(passed_graphs, list):
        raise TypeError("Passed graphs must be a list.")
    if not isinstance(history_filename, str):
        raise TypeError("History filename must be a string.")

    if output_count > input_count:
        raise ValueError("Output count must be less than or equal to input count.")
    if len(passed_graphs) > 20:
        raise ValueError("The number of recently passed graphs must be less than or equal to 20.")
    if len(passed_graphs) < 20 and len(passed_graphs) != output_count:
        raise ValueError("The number of recently passed graphs must be equal to output count if fewer than 20.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recent_passed = passed_graphs[-20:]
    filter_str = json.dumps(rules)

    with open(history_filename, "a") as history_file:
        history_file.write(f"{timestamp}\t{input_count}\t{output_count}\t{filter_str}\t{recent_passed}\n")



def main():
    if len(sys.argv) != 1:
        print("Usage: python graph_filter.py <rules_json>", file=sys.stderr)
        sys.exit(1)

    rules_str = sys.argv[1]
    rules = parse_rules(rules_str)
    validate_rules(rules)

    input_count = 0
    output_count = 0
    passed_graphs = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        input_count += 1

        try:
            G = nx.from_graph6_bytes(line.encode())
        except Exception as e:
            print(f"Error parsing graph: {e}", file=sys.stderr)
            continue

        if passes_all_rules(G, rules):
            print(line)
            passed_graphs.append(line)
            output_count += 1

    history_filename = f"history_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log"
    save_history(rules, input_count, output_count, passed_graphs, history_filename)

    return input_count, output_count, passed_graphs

if __name__ == "__main__":
    main()