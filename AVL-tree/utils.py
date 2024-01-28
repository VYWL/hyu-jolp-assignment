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

def save_tree_to_csv(avl_tree, filename):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        write_tree_node(avl_tree.root, csv_writer)

def write_tree_node(node, csv_writer):
    if node is not None:
        write_tree_node(node.left, csv_writer)
        csv_writer.writerow([node.key, node.value])
        write_tree_node(node.right, csv_writer)

def save_tree_deletion(avl_tree, deleted_keys, filename):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        write_tree_deletion(avl_tree.root, deleted_keys, csv_writer)
        for deleted_key in deleted_keys:
            csv_writer.writerow([deleted_key, "N/A"])

def write_tree_deletion(node, deleted_keys, csv_writer):
    if node is not None:
        write_tree_deletion(node.left, deleted_keys, csv_writer)
        if node.key not in deleted_keys:
            csv_writer.writerow([node.key, node.value])
        write_tree_deletion(node.right, deleted_keys, csv_writer)