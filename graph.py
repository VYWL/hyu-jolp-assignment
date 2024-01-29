class Node:
    def __init__(self, t):
        self.keys = []
        self.values = []
        self.children = []
        self.leaf = True
        self.parent = None

class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t # t: Node 내 최대 key-value 쌍의 개수를 결정

    def search_node(self, key, node=None):
        if self.root is None:
            return None

        current_node = self.root if node is None else node
        while not current_node.leaf:
            for i, item in enumerate(current_node.keys):
                if key == item:
                    return current_node # current_node.values[i]
                elif key < item:
                    current_node = current_node.children[i]
                    break
            else:
                current_node = current_node.children[len(current_node.keys)]
        
        for i, item in enumerate(current_node.keys):
            if key == item:
                return current_node # current_node.values[i]
            
        return None

    def insert_node(self, key, value):
        if self.root is None:
            self.root = Node(self.t)
            self.root.keys.append(key)
            self.root.values.append(value)
        else:
            self._insert_node(key, value, self.root)
        
    def _insert_node(self, key, value, node):
        if key in node.keys:
            return 

        left, right = 0, len(node.keys) - 1
        while left <= right:
            mid = (left + right) // 2
            if node.keys[mid] < key:
                left = mid + 1
            else:
                right = mid - 1
        insert_pos = left

        if node.leaf:
            node.keys.insert(insert_pos, key)
            node.values.insert(insert_pos, value)
        else:
            child = node.children[insert_pos] if insert_pos < len(node.children) else node.children[-1]
            self._insert_node(key, value, child)
            
        if len(node.keys) > 2 * self.t - 1:
            self.split_node(node)

    def split_node(self, node_to_split):
        t = self.t
        new_node = Node(t)
        mid_index = len(node_to_split.keys) // 2 

        new_node.keys = node_to_split.keys[mid_index + 1:]
        new_node.values = node_to_split.values[mid_index + 1:]
        
        mid_key = node_to_split.keys[mid_index]
        mid_value = node_to_split.values[mid_index]
        
        node_to_split.keys = node_to_split.keys[:mid_index]
        node_to_split.values = node_to_split.values[:mid_index]

        if not node_to_split.leaf:
            new_node.children = node_to_split.children[mid_index + 1:]
            node_to_split.children = node_to_split.children[:mid_index + 1]
            for child in new_node.children:
                child.parent = new_node

        new_node.leaf = node_to_split.leaf
        new_node.parent = node_to_split.parent

        if node_to_split == self.root:
            new_root = Node(t)
            new_root.keys.append(mid_key)
            new_root.values.append(mid_value)
            new_root.children.append(node_to_split)
            new_root.children.append(new_node)
            new_root.leaf = False
            self.root = new_root
            node_to_split.parent = new_root
            new_node.parent = new_root
        else:
            parent = node_to_split.parent
            insert_index = self._find_insert_index(parent.keys, mid_key)
            parent.keys.insert(insert_index, mid_key)
            parent.values.insert(insert_index, mid_value)
            parent.children.insert(insert_index + 1, new_node)

    def _find_insert_index(self, keys, key_to_insert):
        left, right = 0, len(keys) - 1
        while left <= right:
            mid = (left + right) // 2
            if keys[mid] < key_to_insert:
                left = mid + 1
            else:
                right = mid - 1
        return left
        
    def delete_node(self, key, node=None):
        if self.root is None:
            return

        if node is None:
            node = self.root

        left, right = 0, len(node.keys) - 1
        while left <= right:
            mid = (left + right) // 2
            if node.keys[mid] < key:
                left = mid + 1
            else:
                right = mid - 1
        i = left

        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                del node.keys[i]
                del node.values[i]
                self._fix_node_after_deletion(node)
            else:
                left_child = node.children[i]
                right_child = node.children[i + 1]
                if len(left_child.keys) >= self.t:
                    pred_key, pred_value = self.get_predecessor(left_child)
                    node.keys[i] = pred_key
                    node.values[i] = pred_value
                    self.delete_node(pred_key, left_child)
                elif len(right_child.keys) >= self.t:
                    succ_key, succ_value = self.get_successor(right_child)
                    node.keys[i] = succ_key
                    node.values[i] = succ_value
                    self.delete_node(succ_key, right_child)
                else:
                    self.merge_nodes(node, i)
                    self.delete_node(key, left_child)
        else:
            if node.leaf:
                return
            flag = (i == len(node.keys))
            if len(node.children[i].keys) < self.t:
                self.fill_node(node, i)

            if flag and i > len(node.keys):
                self.delete_node(key, node.children[i - 1])
            else:
                self.delete_node(key, node.children[i])

    def get_predecessor(self, node):
        # 왼쪽 자식에서 가장 큰 키 찾기
        while not node.leaf:
            node = node.children[len(node.children) - 1]
        return node.keys[len(node.keys) - 1], node.values[len(node.values) - 1]

    def get_successor(self, node):
        # 오른쪽 자식에서 가장 작은 키 찾기
        while not node.leaf:
            node = node.children[0]
        return node.keys[0], node.values[0]

    def _fix_node_after_deletion(self, node):
        if node == self.root:
            if len(node.keys) == 0 and not node.leaf:
                self.root = node.children[0]
                node.children[0].parent = None
            return

        if len(node.keys) < self.t - 1:
            self.fill_node(node)

    def merge_nodes(self, parent_node, idx):
        child = parent_node.children[idx]
        sibling = parent_node.children[idx + 1]

        child.keys.append(parent_node.keys[idx])
        child.values.append(parent_node.values[idx])

        for k, v in zip(sibling.keys, sibling.values):
            child.keys.append(k)
            child.values.append(v)

        if not child.leaf:
            for c in sibling.children:
                child.children.append(c)

        parent_node.keys.pop(idx)
        parent_node.values.pop(idx)
        parent_node.children.pop(idx + 1)

        if parent_node == self.root and len(parent_node.keys) == 0:
            self.root = child
            child.parent = None

    def fill_node(self, node, idx):
        # 현재 노드가 최소 키 수보다 적은 경우

        if idx != 0 and len(node.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(node, idx)
        elif idx != len(node.keys) and len(node.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(node, idx)
        else:
            if idx != len(node.keys):
                self.merge_nodes(node, idx)
            else:
                self.merge_nodes(node, idx - 1)

    def borrow_from_prev(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx - 1]

        child.keys.insert(0, node.keys[idx - 1])
        child.values.insert(0, node.values[idx - 1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

        node.keys[idx - 1] = sibling.keys.pop()
        node.values[idx - 1] = sibling.values.pop()

    def borrow_from_next(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys.append(node.keys[idx])
        child.values.append(node.values[idx])

        node.keys[idx] = sibling.keys.pop(0)
        node.values[idx] = sibling.values.pop(0)

        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))
            
    '''
        FOR DEBUGGING
        - 출력함수만 존재
    '''
    def _collect_nodes(self, node, level, nodes):
        if node is None:
            return

        if len(nodes) <= level:
            nodes.append([])

        node_representation = '(' + ', '.join(f'{k}:{v}' for k, v in zip(node.keys, node.values)) + ')'
        nodes[level].append(node_representation)

        if not node.leaf:
            for child in node.children:
                self._collect_nodes(child, level + 1, nodes)

    def print_tree(self):
        nodes = []
        self._collect_nodes(self.root, 0, nodes)

        for level, nodes_at_level in enumerate(nodes):
            # 각 레벨에서 노드 간의 간격을 계산
            indent = 40 // (2 ** level)
            print(f'Level {level}: {" " * indent}{(" " * indent).join(nodes_at_level)}')
