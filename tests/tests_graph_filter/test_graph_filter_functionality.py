from graph_filter import *


def test_passes_min_rule_tiny_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rules = [{"type": "min", "count": 1, "sum": 3}]
    assert passes_all_rules(G, rules)

def test_passes_min_rule_large_graph():
    G = nx.complete_graph(10)
    rules = [{"type": "min", "count": 20, "sum": 18}]
    assert passes_all_rules(G, rules)

def test_passes_min_rule_medium_graph():
    G = nx.cycle_graph(6)
    rules = [{"type": "min", "count": 5, "sum": 4}]
    assert passes_all_rules(G, rules)


def test_fails_min_rule_tiny_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1)])
    rules = [{"type": "min", "count": 2, "sum": 2}]
    assert not passes_all_rules(G, rules)

def test_fails_min_rule_large_graph():
    G = nx.grid_2d_graph(3, 4)
    G = nx.convert_node_labels_to_integers(G)
    rules = [{"type": "min", "count": 5, "sum": 10}]
    assert not passes_all_rules(G, rules)

def test_fails_min_rule_medium_graph():
    G = nx.path_graph(7)
    rules = [{"type": "min", "count": 2, "sum": 5}]
    assert not passes_all_rules(G, rules)



def test_passes_max_rule_tiny_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])
    rules = [{"type": "max", "count": 2, "sum": 3}]
    assert passes_all_rules(G, rules)

def test_passes_max_rule_medium_graph():
    G = nx.star_graph(6)
    rules = [{"type": "max", "count": 6, "sum": 7}]
    assert passes_all_rules(G, rules)

def test_passes_max_rule_large_graph():
    G = nx.balanced_tree(2, 3)
    rules = [{"type": "max", "count": 10, "sum": 6}]
    assert passes_all_rules(G, rules)


def test_fails_max_rule_tiny_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
    rules = [{"type": "max", "count": 1, "sum": 3}]
    assert not passes_all_rules(G, rules)

def test_fails_max_rule_large_graph():
    G = nx.hexagonal_lattice_graph(3,2)
    G = nx.convert_node_labels_to_integers(G)
    rules = [{"type": "max", "count": 1, "sum": 5}]
    assert not passes_all_rules(G, rules)

def test_fails_max_rule_medium_graph():
    G = nx.wheel_graph(7)
    rules = [{"type": "max", "count": 2, "sum": 6}]
    assert not passes_all_rules(G, rules)



def test_passes_exact_rule_tiny_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    rules = [{"type": "exact", "count": 3, "sum": 4}]
    assert passes_all_rules(G, rules)

def test_passes_exact_rule_large_graph():
    G = nx.barbell_graph(5, 5)
    rules = [{"type": "exact", "count": 3, "sum": 4}]
    assert passes_all_rules(G, rules)

def test_passes_exact_rule_medium_graph():
    G = nx.lollipop_graph(5, 3)
    rules = [{"type": "exact", "count": 2, "sum": 9}]
    assert passes_all_rules(G, rules)


def test_fails_exact_rule_tiny_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rules = [{"type": "exact", "count": 2, "sum": 3}]
    assert not passes_all_rules(G, rules)

def test_fails_exact_rule_large_graph():
    G = nx.circulant_graph(12, [1, 5])
    rules = [{"type": "exact", "count": 20, "sum": 6}]
    assert not passes_all_rules(G, rules)

def test_fails_exact_rule_medium_graph():
    G = nx.house_graph()
    G.add_nodes_from([5, 6, 7])
    G.add_edges_from([(2, 5), (5, 6), (6, 7)])
    rules = [{"type": "exact", "count": 2, "sum": 6}]
    assert not passes_all_rules(G, rules)



def test_passes_combination_of_min_max_rules():
    G = nx.house_x_graph()
    rules = [{"type": "min", "count": 2, "sum": 7}, {"type": "max", "count": 1, "sum": 8}]
    assert passes_all_rules(G, rules)

def test_fails_combination_of_min_max_rules():
    G = nx.ladder_graph(4)
    rules = [{"type": "min", "count": 3, "sum": 4}, {"type": "max", "count": 6, "sum": 6}]
    assert not passes_all_rules(G, rules)


def test_passes_combination_of_min_max_rules_same_number_of_edges():
    G = nx.petersen_graph()
    rules = [{"type": "min", "count": 15, "sum": 6}, {"type": "max", "count": 15, "sum": 6}]
    assert passes_all_rules(G, rules)

def test_fails_combination_of_min_max_rules_same_number_of_edges():
    G = nx.empty_graph(10)
    rules = [{"type": "min", "count": 1, "sum": 10}, {"type": "max", "count": 1, "sum": 10}]
    assert not passes_all_rules(G, rules)



def test_passes_combination_of_min_exact_rules():
    G = nx.bull_graph()
    rules = [{"type": "min", "count": 2, "sum": 4}, {"type": "exact", "count": 1, "sum": 6}]
    assert passes_all_rules(G, rules)

def test_fails_combination_of_min_exact_rules():
    G = nx.diamond_graph()
    rules = [{"type": "min", "count": 3, "sum": 5}, {"type": "exact", "count": 1, "sum": 6}]
    assert not passes_all_rules(G, rules)



def test_passes_combination_of_max_exact_rules():
    G = nx.tetrahedral_graph()
    rules = [{"type": "max", "count": 7, "sum": 6}, {"type": "exact", "count": 6, "sum": 6}]
    assert passes_all_rules(G, rules)

def test_fails_combination_of_max_exact_rules():
    G = nx.circular_ladder_graph(5)
    rules = [{"type": "max", "count": 10, "sum": 6}, {"type": "exact", "count": 15, "sum": 4}]
    assert not passes_all_rules(G, rules)



def test_passes_combination_of_two_min_rules():
    G = nx.windmill_graph(4, 3)
    rules = [{"type": "min", "count": 4, "sum": 10}, {"type": "min", "count": 2, "sum": 4}]
    assert passes_all_rules(G, rules)

def test_fails_combination_of_two_min_rules():
    G = nx.windmill_graph(4, 3)
    rules = [{"type": "min", "count": 6, "sum": 4}, {"type": "min", "count": 9, "sum": 10}]
    assert not passes_all_rules(G, rules)


def test_passes_combination_of_two_max_rules():
    G = nx.windmill_graph(4, 3)
    rules = [{"type": "max", "count": 8, "sum": 10}, {"type": "max", "count": 4, "sum": 4}]
    assert passes_all_rules(G, rules)

def test_fails_combination_of_two_max_rules():
    G = nx.windmill_graph(4, 3)
    rules = [{"type": "max", "count": 6, "sum": 10}, {"type": "max", "count": 3, "sum": 4}]
    assert not passes_all_rules(G, rules)