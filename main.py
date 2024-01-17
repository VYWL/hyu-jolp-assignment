from graph import AVLTree

def main():
    avl_tree = AVLTree()

    while(1):
        new_input = int(input("새 숫자 입력(0: quit): "))
        if new_input == 0:
            break
        print(f'========== {new_input} - insertion ==========')
        avl_tree.insert_node(new_input)
        # 트리 출력 (디버깅 용도)
        avl_tree.print_tree_horizontal()
        print(f'========== {new_input} - insertion ==========\n\n')
        
        
    while(1):
        new_input = int(input("새 숫자 입력(0: quit): "))
        if new_input == 0:
            break
        print(f'========== {new_input} - deletion ==========')
        avl_tree.delete_node(new_input)
        # 트리 출력 (디버깅 용도)
        avl_tree.print_tree_horizontal()
        print(f'========== {new_input} - deletion ==========\n\n')


if __name__ == "__main__":
    main()
