from flask import Flask, render_template, request, redirect, url_for
import os
import shutil
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_GRAPHS_DIR = os.path.join(BASE_DIR, "static", "graphs")
HISTORY_DIR = os.path.expanduser("~/.history")
IMAGE_DIR = os.path.expanduser("~/.graph_images")

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))


@app.route('/index')
def index():
    latest_history_file = find_latest_history_file()
    recent_graphs = parse_recent_graphs(latest_history_file)

    latest_image_folder = find_latest_image_folder()
    copy_images_to_static(latest_image_folder)
    graph_images = list_graph_images()

    paired_data = list(zip(recent_graphs, graph_images))

    return render_template("index.html", recent_graphs=recent_graphs, paired_data=paired_data)


@app.route('/generate', methods=['POST'])
def generate():
    filter_rule = request.form.get("filter_rule")
    nb_vertices = request.form.get("nb_vertices")

    try:
        n = int(nb_vertices)
    except ValueError:
        print("The number of vertices is not an integer.")
        return "Invalid number of vertices.", 400

    success = run_graph_filter(n, filter_rule)

    if not success:
        return "Failed to generate graphs.", 500

    return redirect(url_for("index"))


def find_latest_history_file():
    if not os.path.exists(HISTORY_DIR):
        print(f"History directory {HISTORY_DIR} doesn't exist. Creating it.")
        os.makedirs(HISTORY_DIR, exist_ok=True)

    files = []

    for file in os.listdir(HISTORY_DIR):
        if file.endswith(".log"):
            files.append(os.path.join(HISTORY_DIR, file))

    if not files:
        return None

    return max(files, key=os.path.getmtime)

def find_latest_image_folder():
    if not os.path.exists(IMAGE_DIR):
        print(f"Image directory {IMAGE_DIR} doesn't exist. Creating it.")
        os.makedirs(IMAGE_DIR, exist_ok=True)

    image_folders = []

    for folder in os.listdir(IMAGE_DIR):
        if folder.startswith("recently_passed_graphs"):
            image_folders.append(os.path.join(IMAGE_DIR, folder))

    if not image_folders:
        return None

    return max(image_folders, key=os.path.getmtime)


def parse_recent_graphs(filepath):
    if not filepath:
        print("No history file found.")
        return []

    try:
        with open(filepath, "r") as file:
            entry = file.read()
            entry = entry.strip().split("\t")

        if len(entry) != 5:
            print("Invalid history entry format.")
            return []

        return eval(entry[-1])

    except Exception as e:
        print(f"Error parsing graph list: {e}")
        return []


def copy_images_to_static(image_folder):
    if not image_folder:
        print("No image folder found.")
        return

    os.makedirs(STATIC_GRAPHS_DIR, exist_ok=True)

    try:
        for image in os.listdir(image_folder):
            src = os.path.join(image_folder, image)
            dst = os.path.join(STATIC_GRAPHS_DIR, image)
            shutil.copy(src, dst)

    except Exception as e:
        print(f"Error copying images: {e}")


def extract_graph_number(image_name):
    number_part = image_name.split("_")[1]
    number_str = number_part.split(".")[0]
    return int(number_str)


def list_graph_images():
    graph_images = []
    sorted_static_graph_im = sorted(os.listdir(STATIC_GRAPHS_DIR), key = extract_graph_number)

    for im in sorted_static_graph_im:
        graph_images.append(im)
    return graph_images


def run_graph_filter(n, rules):
    script_path = os.path.join(BASE_DIR, "graph_filter", "run_filter.sh")

    command = ["bash", script_path, str(n), rules, "--export", "--image_format", "png"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print("Script error:", result.stderr)
            return False

        return True

    except Exception as e:
        print(f"Error running graph filter: {e}")
        return False

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
