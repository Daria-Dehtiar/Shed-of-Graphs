from graph_filter.filter_util import *


def main():
    if len(sys.argv) < 3:
        print("Usage: python filter_main.py <rules_json> <history_filename> [--export image_folder] [--image_format"
              "format]", file=sys.stderr)
        sys.exit(1)


    rules_str = sys.argv[1]
    history_filename = sys.argv[2]


    export_dir = None
    image_format = None

    if "--export" in sys.argv:
        index = sys.argv.index("--export")
        if (index + 1) < len(sys.argv) and not sys.argv[index + 1].startswith("--"):
            export_dir = sys.argv[index + 1]
        else:
            export_dir = os.path.expanduser("~/.graph_images")

    if "--image_format" in sys.argv:
        index = sys.argv.index("--image_format")
        if (index + 1) < len(sys.argv) and not sys.argv[index + 1].startswith("--"):
            image_format = sys.argv[index + 1]
        else:
            image_format = "png"


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
            passed_graphs.append(line)
            output_count += 1

    recent_passed = passed_graphs[-20:]


    save_history(rules, input_count, output_count, recent_passed, history_filename)


    if export_dir and image_format:
        export_graphs(recent_passed, export_dir, image_format)


    return input_count, output_count, passed_graphs



if __name__ == "__main__":
    main()