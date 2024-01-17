class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

    def update_height(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1

    def get_balance_factor(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

class AVLTree:
    def __init__(self):
        self.root = None

    def insert_node(self, key) -> None:
        '''
            insert_node(key)
            : Tree의 적절한 위치에 Node를 삽입 후 root 초기화,
            - 이미 있는 노드이면 삽입을 하지 않음
        '''
        if self.search_node(key) is not None:
            return
        
        self.root = self._insert_node(self.root, key)
    
    def _insert_node(self, node: Node, key):
        '''
            - root가 None이라면 (아무것도 없다면) root에 삽입
            - 아니라면 재귀를 통해 찾아감
            - 넣고 나서, check_status 함수를 호출해서 balance check
        '''
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert_node(node.left, key)
        else:
            node.right = self._insert_node(node.right, key)
            
        return self.rebalance_tree(node)

    def search_node(self, key) -> Node:
        '''
            search_node(key)
            : key를 기준으로 Tree에 해당 key의 Node가 있는지 찾아주는 함수
        '''
        return self._search_node(self.root, key)
    
    def _search_node(self, node: Node, key):
        '''
            - 찾았다면, Node를 return
            - 못 찾았다면, None 반환
        '''
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._search_node(node.left, key)
        else :
            return self._search_node(node.right, key)


    def delete_node(self, key):
        '''
            delete_node(key)
            : key를 기준으로 찾은 Node를 삭제
                - Tree에 없는 key라면, 아무일이 일어나지 않음
        '''
        if self.search_node(key) is  None:
            return
        
        self.root = self._delete_node(self.root, key) 
    
    def _delete_node(self, node: Node, key):
        '''
            - 해당 Node의 left child가 있다면
                - 그 중 가장 큰 원소를 찾아서 바꾼뒤에 해당 원소(left child 중 젤 큰거)삭제
                - upwind 하면서 check_status 함수를 호출해서 balance check
            - left child가 없다면
                - right child를 현재 Node로 대체후, upwind 하면서 rebalance 함수를 호출해서 balance check
            - right child도 없다면
                - 그냥 삭제 후 upwind 하면서 rebalance 함수를 호출해서 balance check
        '''
        if node is None:
            return node

        # search랑 아이디어는 같음 -> 재귀로 타고타고 감
        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # child가 없는 경우
            if node.height == 1:
                return None
            
            # 낱개 child가 있는 경우
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Copy
            max_value_node = self.get_max_value_node(node.left)
            node.key = max_value_node.key
            node.left = self._delete_node(node.left, max_value_node.key)
            
        return self.rebalance_tree(node)
            
    def get_max_value_node(self, node: Node) -> Node:
        '''
            자식중 가장 큰 key값을 찾음
        '''
        if node is None or node.right is None:
            return node
        
        return self.get_max_value_node(node.right)
            
   
    def rebalance_tree(self, node: Node):
        ''''
            rebalance_tree(node)
            : Operation 이후, balance가 무너지지 않았는지 확인하는 함수
                만약, 해당 key Node 중심으로 근처 BF를 확인하고
                적절히 case check(LL, LR, RL, RR) 후에 호출
        '''
        if node is None:
            return None
        
        node.update_height()
        balance_factor = node.get_balance_factor()
        
        # LL Case
        if balance_factor > 1 and node.left.get_balance_factor() >= 0:
            return self.rotate_right(node)
        
        # LR Case
        if balance_factor > 1 and node.left.get_balance_factor() < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        # RL Case
        if balance_factor < -1 and node.right.get_balance_factor() > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        # RR Case
        if balance_factor < -1 and node.right.get_balance_factor() <= 0:
            return self.rotate_left(node)
        
        return node
    
    '''
        기본 회전 관련 함수
    '''
    
    def rotate_left(self, y):
        '''
            해당 key를 기준을 rotating right를 수행하는 함수 (가장 아래있는 노드부터, x, y, z)
                1. y노드의 오른쪽 자식 노드를 z노드로 변경.
                2. z노드 왼쪽 자식 노드를 y노드 오른쪽 서브트리(T2)로 변경합니다.
                3. y를 새로운 루트 노드로 설정.
        '''
        x = y.right
        T2 = x.left

        # rotation
        x.left = y
        y.right = T2

        # Update heights
        y.update_height()
        x.update_height()

        return x
    
    def rotate_right(self, x):
        '''
            해당 key를 기준을 rotating left를 수행하는 함수  (가장 아래있는 노드부터, x, y, z)
                y노드의 왼쪽 자식 노드를 z노드로 변경.
                z노드 오른쪽 자식 노드를 y노드 왼쪽 서브트리(T2)로 변경.
                y를 새로운 루트 노드로 설정.
        '''
        y = x.left
        T3 = y.right

        # rotation
        y.right = x
        x.left = T3

        # Update heights
        x.update_height()
        y.update_height()

        return y

    def print_tree(self, node=None, level=0, max_height=None):
        if node is None:
            node = self.root
            if node is None:
                return
            max_height = self.root.height  # 트리의 전체 높이를 설정

        # 최대 높이를 넘어가면 출력하지 않고 반환
        if level >= max_height:
            return

        # 오른쪽 자식이 있는 경우, 더 깊은 레벨로 재귀 호출
        if node.right is not None:
            self.print_tree(node.right, level + 1, max_height)

        print(' ' * 4 * level + '->', node.key)

        # 왼쪽 자식이 있는 경우, 더 깊은 레벨로 재귀 호출
        if node.left is not None:
            self.print_tree(node.left, level + 1, max_height)
            

    def _fill_levels(self, node, level, levels, left, right):
        if node is None:
            return

        mid = (left + right) // 2
        levels[level][mid] = str(node.key)

        self._fill_levels(node.left, level + 1, levels, left, mid - 1)
        self._fill_levels(node.right, level + 1, levels, mid + 1, right)

    def print_tree_horizontal(self):
        if self.root is None:
            return
        
        height = self.root.height
        width = 2 ** height - 1
        levels = [[' ' for _ in range(width)] for _ in range(height)]

        self._fill_levels(self.root, 0, levels, 0, width - 1)

        for level in levels:
            print(''.join(level))


