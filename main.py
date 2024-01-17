from graph import AVLTree

def main():
    avl_tree = AVLTree()

    while(1):
        new_key = int(input("새 키 입력(0: quit): "))
        new_value = int(input("새 값 입력: "))
        if new_key == 0:
            break
        print(f'========== {new_key}, {new_value} - insertion ==========')
        avl_tree.insert_node(new_key, new_value)
        # 트리 출력 (디버깅 용도)
        avl_tree.print_tree_horizontal()
        print(f'========== {new_key}, {new_value} - insertion ==========\n\n')
        
        
    while(1):
        new_key = int(input("새 키 입력(0: quit): "))
        if new_key == 0:
            break
        print(f'========== {new_key} - deletion ==========')
        avl_tree.delete_node(new_key)
        # 트리 출력 (디버깅 용도)
        avl_tree.print_tree_horizontal()
        print(f'========== {new_key} - deletion ==========\n\n')


if __name__ == "__main__":
    main()
