# Shed of Graphs

This is a web application for filtering graphs based on user-defined criteria, visualizing them and keeping a processing log. It is implemented as a Flask web-server with result saving and ability to view to graph images directly in the browser. 

## Features
- Generate graphs using `nauty-geng`
- Filter graphs based on rules, e.g.: minimum 3 edges where the sum of the degrees
 of the incident vertices is 5 and maximum 5 edges where the sum of the
 degrees of the incident vertices is 6
- Export results as `.g6`-lines and `.png`images
- Keep a processing log with timestamps, filtering rules, and passed graphs
- Provide a web interface for convenient interaction with the backend
- Create hourly backups of history logs
- Support running via Docker

## Running

### Without Docker
````bash
sudo apt install python3 python3-venv python3-pip nauty
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 web_server.py
````

### With Docker
````bash
docker build -t shed-of-graphs .
docker run -it --rm -p 5000:5000 \
-v $HOME/.history:/root/.history \
shed-of-graphs
````
After running search for:
``http://localhost:5000/index``

## Interface

The web interface allows you to:

- Enter the number of vertices
- Enter a filter rule as a JSON string
- Generate and filter graphs based on your criteria
- View a table of the most recent graphs that passed the filter
- See visual representation of those graphs

## Example Filter Rules

Each rule defines a constraint on number of edges in a graph where the sum of degrees of the incident vertices meets a condition.

### 1. Minimum edge constraint
At least 3 edges must have a degree sum of 5.
````json
{"type": "min", "count": 3, "sum": 5}
````

### 2. Maximum edge constraint
No more than 5 edges may have a degree sum of 6.
````json
{"type": "max", "count": 5, "sum": 6}
````

### 3. Exact edge constraint
Exactly 2 edges must have a degree sum of 4.
````json
{"type": "exact", "count": 2, "sum": 4}
````

### 4. Combined rule
Multiple constraints should be combined in a list.
````json
[
 {"type": "min", "count": 3, "sum": 5},
  {"type": "max", "count": 5, "sum": 6}
]
````

## Testing

````bash
pytest tests/
````
Covers:
- Graph filtering logic
- History saving functionality

## Log and backup

The processing history is saved in the `~/.history` directory. To enable automatic backups, run:
````bash 
bash enable_backup_history.sh
````
Then backups will be created automatically in `~/.filtered-graphs` directory. Images of the most recently passed graphs are stored in ``~/.graph_images``.

## Author
[Daria Dehtiar](mailto:daria.dehtiar@student.kuleuven.be)