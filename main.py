# main.py
from graph import BTree
from utils import *
from valid import *

def main():
    target_tree = BTree()

    while True:
        print("1. Insertion\n2. Deletion\n3. Quit")
        choice = input("Choose an operation: ")

        if choice == "1":
            filename = input("Enter filename for insertion: ")
            perform_insertion_and_validation(target_tree, filename)
        elif choice == "2":
            deletion_filename = input("Enter filename for deletion: ")
            compare_filename = input("Enter filename for delete comparison: ")
            perform_deletion_and_validation(target_tree, deletion_filename, compare_filename)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
