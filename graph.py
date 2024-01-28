class Node:
    def __init__(self, t):
        self.keys = []
        self.values = []
        self.children = []
        self.leaf = True

class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t # t: Node 내 최대 key-value 쌍의 개수를 결정

    def search_node(self, key, node=None) -> Node:
        if self.root is None:
            return None
        
        if node is None:
            node = self.root
            
        for i, item in enumerate(node.keys):
            if key == item:
                return node.values[i]

        if node.leaf:
            return None

        for i in range(len(node.keys)):
            if key < node.keys[i]:
                return self.search_node(key, node.children[i])
        return self.search_node(key, node.children[len(node.keys)])

    def insert_node(self, key, value):
        if self.search_node(key) is not None:
            return

        if self.root is None:
            self.root = Node(self.t)
            self.root.keys.append(key)
            self.root.values.append(value)
        else:
            self._insert_node(key, value, self.root)
            
        
    def _insert_node(self, key, value, node: Node):
        if node.leaf:
            # Leaf node에서는 직접 삽입
            node.keys.append(key)
            node.values.append(value)
            node.keys, node.values = zip(*sorted(zip(node.keys, node.values)))
            node.keys = list(node.keys)
            node.values = list(node.values)
        else:
            # 위치 찾아서 삽입
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            self._insert_node(key, value, node.children[i])
            
        if len(node.keys) > 2 * self.t - 1:
            self.split_node(node)


    def split_node(self, node_to_split):
        t = self.t
        
        mid_index = len(node_to_split.keys) // 2 - 1
        mid_key = node_to_split.keys[mid_index]
        mid_value = node_to_split.values[mid_index]

        left_child = Node(t)
        left_child.keys = node_to_split.keys[:mid_index]
        left_child.values = node_to_split.values[:mid_index]
        right_child = Node(t)
        right_child.keys = node_to_split.keys[mid_index + 1:]
        right_child.values = node_to_split.values[mid_index + 1:]

        if not node_to_split.leaf:
            left_child.children = node_to_split.children[:mid_index + 1]
            right_child.children = node_to_split.children[mid_index + 1:]
            left_child.leaf = False
            right_child.leaf = False

        if node_to_split == self.root:
            new_root = Node(t)
            new_root.keys = [mid_key]
            new_root.values = [mid_value]
            new_root.children = [left_child, right_child]
            new_root.leaf = False
            self.root = new_root
        else:
            parent = self._find_parent(self.root, node_to_split)
            if parent is None:
                return
            
            insert_index = self._find_insert_index(parent.keys, mid_key)
            parent.keys.insert(insert_index, mid_key)
            parent.values.insert(insert_index, mid_value)
            parent.children[insert_index] = left_child
            parent.children.insert(insert_index + 1, right_child)

            if len(parent.keys) > 2 * t - 1:
                self.split_node(parent)

    def _find_insert_index(self, keys, key_to_insert):
        for i, key in enumerate(keys):
            if key_to_insert < key:
                return i
        return len(keys)
    
    def _find_parent(self, parent, child):
        if parent.leaf or child in parent.children:
            return parent
        for node_child in parent.children:
            if child in node_child.children:
                return self._find_parent(node_child, child)
        return None
        
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
