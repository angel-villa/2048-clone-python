import copy

class DecisionNode:

    __slots__ = 'board', 'move_path', 'max_depth', 'depth', 'max_val', 'corner_val', \
                'score', 'parent', 'up', 'left', 'down', 'right', 'left_col_sum', \
                'weighted_sum'
                
    def __init__(self, board, max_depth, move_path=[], depth=0):
        self.board = board
        self.max_depth = max_depth
        self.move_path = move_path
        self.depth = depth
        
        # metrics, need to find a better way to measure success
        self.max_val = self.board.max_tile()
        self.corner_val = self.board.corner_tile()
        self.left_col_sum = self.board.left_col_sum()
        self.score = self.board.score
        self.weighted_sum = self.board.top_right_weighted_sum()
        
        # pointers
        self.parent = None
        self.up = None
        self.left = None
        self.down = None
        self.right = None
        
        # limit the tree height to max_depth
        if self.depth < max_depth:
            self.make_children()
        
    # make 'up' or 'right' children for each node if the board can shift in either of those directions
    # else try to make 'down' and 'left' children
    def make_children(self):
        if self.board.can_shift_up():
            temp_up = copy.deepcopy(self.board)
            temp_up.shift('w')
            self.up = DecisionNode(temp_up, self.max_depth, self.move_path, self.depth + 1)
            self.up.set_parent(self.board)
            self.up.move_path.append('w')
        if self.board.can_shift_right():
            temp_right = copy.deepcopy(self.board)
            temp_right.shift('d')
            self.right = DecisionNode(temp_right, self.max_depth, self.move_path, self.depth + 1)
            self.right.set_parent(self.board)
            self.right.move_path.append('d')
        elif not (self.board.can_shift_up() or self.board.can_shift_right()):
            if self.board.can_shift_down():
                temp_down = copy.deepcopy(self.board)
                temp_down.shift('s')
                self.down = DecisionNode(temp_down, self.max_depth, self.move_path, self.depth + 1)
                self.down.set_parent(self.board)
                self.down.move_path.append('s')
            if self.board.can_shift_left():
                temp_left = copy.deepcopy(self.board)
                temp_left.shift('a')
                self.left = DecisionNode(temp_left, self.max_depth, self.move_path, self.depth + 1)
                self.left.set_parent(self.board)
                self.left.move_path.append('a')
        else:
            pass

    def set_parent(self, node):
        self.parent = node