# main.py
from graph import BTree
from utils import *
from valid import *

isDev= False

def main():
    target_tree = BTree(t=31)

    if isDev:
        while True:
            new_key = int(input("새 키 입력(0: quit): "))
            new_value = new_key  # int(input("새 값 입력: "))
            if new_key == 0:
                break
            print(f'========== {new_key}, {new_value} - insertion ==========')
            target_tree.insert_node(new_key, new_value)
            # 트리 출력 (디버깅 용도)
            target_tree.print_tree()
            print(f'========== {new_key}, {new_value} - insertion ==========\n\n')
            
        return

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
