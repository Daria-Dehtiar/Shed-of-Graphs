import os
import sys


HISTORY_PAR_DIR = os.path.expanduser("~/.history_parallel")
HISTORY_DIR = os.path.expanduser("~/.history")


def parse_line(line):
    parts = line.strip().split("\t")
    if len(parts) != 5:
        raise Exception(f"Unable to parse line: {line}")

    timestamp, input_count, output_count, rule_str, passed_graphs_str = parts
    return {
        "timestamp": timestamp,
            "input count": int(input_count),
            "output count": int(output_count),
            "passed graphs": eval(passed_graphs_str)
    }


def find_matching_files(directory, timestamp, nb_vertices):
    matching_files = []

    for filename in os.listdir(directory):
        if (timestamp in filename) and (str(nb_vertices) in filename):
            matching_files.append(os.path.join(directory, filename))
    return matching_files


def merge_info(matching_files):
    total_input = 0
    total_output = 0
    all_passed_graphs = []

    for full_path in matching_files:
        with open(full_path) as file:
            line = file.readline()
            entry = parse_line(line)

            total_input += entry["input count"]
            total_output += entry["output count"]
            all_passed_graphs.extend(entry["passed graphs"])

    most_recent_passed_graphs = all_passed_graphs[-20:]
    return total_input, total_output, most_recent_passed_graphs


def write_line(line, filename):
    with open(filename, "w") as file:
        file.write(line)
    print(f"Merged history written to: {filename}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_history.py <timestamp> <number_of_vertices> <rules_json>", file=sys.stderr)
        sys.exit(1)

    timestamp = sys.argv[1]
    number_of_vertices = sys.argv[2]
    rules_json = sys.argv[3]

    matching_files = find_matching_files(HISTORY_PAR_DIR, timestamp, number_of_vertices)
    if len(matching_files) == 0:
        print("No matching files to merge", file=sys.stderr)
        sys.exit(1)

    try:
        input_count, output_count, most_recent_passed_graphs = merge_info(matching_files)
    except Exception as e:
        print(f"Error merging info: {e}", file=sys.stderr)
        sys.exit(1)

    new_line = f"{timestamp}\t{input_count}\t{output_count}\t{rules_json}\t{most_recent_passed_graphs}\n"

    os.makedirs(HISTORY_DIR, exist_ok=True)
    filename = f"merged_history_{number_of_vertices}_{timestamp}.log"
    full_path = os.path.join(HISTORY_DIR, filename)

    write_line(new_line, full_path)

if __name__ == "__main__":
    main()