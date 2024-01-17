# main.py
from graph import AVLTree
from utils import read_csv
from tqdm import tqdm
import csv

def save_tree_to_csv(avl_tree, filename):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        save_tree_node(avl_tree.root, csv_writer)

def save_tree_node(node, csv_writer):
    if node is not None:
        save_tree_node(node.left, csv_writer)
        csv_writer.writerow([node.key, node.value])
        save_tree_node(node.right, csv_writer)

def validate_tree(avl_tree, original_data, desc):
    search_score = 0
    compare_score = 0

    for key, value in tqdm(original_data, desc=desc):
        node = avl_tree.search_node(int(key))
        if node is not None:
            search_score += 1
            if node.value == value:
                compare_score += 1

    total = len(original_data)
    print(f"[{desc}]\nsearch_score: {search_score} / {total}\ncompare_score: {compare_score} / {total}")

def perform_insertion(avl_tree, filename):
    data = read_csv(filename)
    
    for key, value in tqdm(data, desc="Inserting data"):
        avl_tree.insert_node(int(key), value)

    save_tree_to_csv(avl_tree, 'inserted_data.csv')
    validate_tree(avl_tree, data, "Insertion & Search")

def perform_deletion(avl_tree, filename):
    data = read_csv(filename)
    for key, _ in tqdm(data, desc="Deleting data"):
        avl_tree.delete_node(int(key))

    validation_data = read_csv('delete_compare.csv')
    validate_tree(avl_tree, validation_data, "Deletion")

def main():
    avl_tree = AVLTree()

    while True:
        print("1. Insertion\n2. Deletion\n3. Quit")
        choice = input("Choose an operation: ")

        if choice == "1":
            filename = input("Enter filename for insertion: ")
            perform_insertion(avl_tree, filename)
        elif choice == "2":
            filename = input("Enter filename for deletion: ")
            perform_deletion(avl_tree, filename)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
