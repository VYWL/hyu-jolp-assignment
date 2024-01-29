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
                    return current_node.values[i]
                elif key < item:
                    current_node = current_node.children[i]
                    break
            else:
                current_node = current_node.children[len(current_node.keys)]
        
        for i, item in enumerate(current_node.keys):
            if key == item:
                return current_node.values[i]
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
