import csv

def read_csv(filename, isComma=False):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            [key, value] = row if isComma else row[0].split('\t')
            data.append((key, value))
    return data

'''
    csv 저장 -> insertion / deletion 목적 구분
'''

def save_tree_to_csv(tree, filename):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        write_tree_node(tree.root, csv_writer)

def write_tree_node(node, csv_writer):
    if node is not None:
        for child in node.children:
            write_tree_node(child, csv_writer)
        for key, value in zip(node.keys, node.values):
            csv_writer.writerow([key, value])

def save_tree_deletion(tree, deleted_keys, filename):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        write_tree_deletion(tree.root, deleted_keys, csv_writer)
        for deleted_key in deleted_keys:
            csv_writer.writerow([deleted_key, "N/A"])

def write_tree_deletion(node, deleted_keys, csv_writer):
    if node is not None:
        for child in node.children[:-1]:
            write_tree_deletion(child, deleted_keys, csv_writer)
        for key, value in zip(node.keys, node.values):
            if key not in deleted_keys:
                csv_writer.writerow([key, value])
        if not node.leaf:
            write_tree_deletion(node.children[-1], deleted_keys, csv_writer)
