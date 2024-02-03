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
                    return current_node
                elif key < item:
                    current_node = current_node.children[i]
                    break
            else:
                current_node = current_node.children[len(current_node.keys)]
        
        for i, item in enumerate(current_node.keys):
            if key == item:
                return current_node
            
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

        ''' 
        [수정사항]
        지난 Insertion만 구현했을때, 새 노드 2개를 정의하고 나서 children의 parent 정보를 수정하지 않아서,
        동일한 split이 두번 이상 일어나는 경우가 생기게 되었음. 이는 매우 느린 처리시간으로 이어짐.
        
        => 기존 노드를 수정 + 새 노드는 오른쪽 자식 노드로 수정하는 방식으로 구조 변경 및 코드 수정
        
        즉, New node는 새로 추가되는 오른쪽 자식 노드가 되고, 기존 노드는 왼쪽 자식 노드가 됨
        '''
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

        # Root의 경우 split 시에 self.root를 갱신해주어야 함.
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
        '''
        [수정사항]
        B-Tree 내 모든 노드의 key는 정렬되어 있기 때문에,
        모든 linear search를 Binary search로 변경하여 속도를 높임.
        => (t=31) 일때 큰 속도 개선
        '''
        
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

        '''
        [수정사항]
        B-Tree 내 모든 노드의 key는 정렬되어 있기 때문에,
        모든 linear search를 Binary search로 변경하여 속도를 높임.
        => (t=31) 일때 큰 속도 개선
        '''
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
                node.keys.pop(i)
                node.values.pop(i)
                self.postprocess_node(node)
            else:
                left_child = node.children[i]
                right_child = node.children[i + 1]
                
                '''
                경우에 따라, 좌측 child의 가장 큰 키 값 혹은 우측 child의 가장 작은 키 값을 조회
                -> 값을 미리 복사하고 재귀를 통해(연쇄적인 merge가 일어날 수 있으므로), 해당 노드를 지우는 방식으로 처리
                '''
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
        while not node.leaf:
            node = node.children[len(node.children) - 1]
        return node.keys[len(node.keys) - 1], node.values[len(node.values) - 1]

    def get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0], node.values[0]

    # 분기 처리하기 귀찮아서 별도 함수에서 후처리 -> key가 없거나 부족한 경우 처리
    def postprocess_node(self, node):
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

    '''
    키 개수가 부족한 경우 borrow 해와야함
    -> index 기준으로 좌우 child 살피고 하나를 가져옴
    '''
    def fill_node(self, node, idx):
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
