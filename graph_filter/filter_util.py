import json
import sys
from datetime import datetime
import networkx as nx
import os
import matplotlib.pyplot as plt


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
        if rule["type"] == "min" and count < rule["count"]:
            return False
        if rule["type"] == "max" and count > rule["count"]:
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
    if len(passed_graphs) != output_count:
        raise ValueError("The number of passed graphs must be equal to output count.")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filter_str = json.dumps(rules)

    with open(history_filename, "a") as history_file:
        history_file.write(f"{timestamp}\t{input_count}\t{output_count}\t{filter_str}\t{passed_graphs}\n")


def export_graphs(graphs, image_folder, image_format):
    if not graphs:
        print("No graphs are found to export.")
        return

    if image_format.lower() not in plt.gcf().canvas.get_supported_filetypes():
        print(f"Image format {image_format} is not supported.", file=sys.stderr)
        sys.exit(1)

    try:
        image_folder_expanded = os.path.expanduser(image_folder)
        os.makedirs(image_folder_expanded, exist_ok=True)

        timestamp_folder = f"recently_passed_graphs_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"
        full_folder_path = os.path.join(image_folder_expanded, timestamp_folder)
        os.makedirs(full_folder_path, exist_ok=True)

    except Exception as e:
        print(f"Failed to create export directory: {e}", file=sys.stderr)
        sys.exit(1)

    for index, graph in enumerate(graphs, 1):
        try:
            G = nx.from_graph6_bytes(graph.encode())

            plt.figure(figsize=(5, 5))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, node_size=25)

            image_file_name = os.path.join(full_folder_path, f"graph_{index:02d}.{image_format}")
            plt.savefig(image_file_name, format=image_format)
            plt.close()

        except Exception as e:
            print(f"Failed to export graph #{index:02d}: {e}", file=sys.stderr)
            continue