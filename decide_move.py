import collections as col
import random

import DecisionNode as dn

# make 100 decision trees and make the most common 'best' move among the trees,
# based on 'best_score' in the 'best_move_in_tree' function
def decide_move(board, max_depth):
    best_moves = []
    for i in range(100):
        root = dn.DecisionNode(board, max_depth, [], 0)
        best_moves.append(best_move_in_tree(root))
    ranked_moves = best_moves_descending(best_moves)
    for move in ranked_moves:
        if board.can_shift(move[0]):
            return move[0]
    for move in ['w', 'd', 's', 'a']:
        if board.can_shift(move):
            return move
    
# do BFS to find the node with the best score, return first move that eventually leads to that node
def best_move_in_tree(node):
    tree_count = 0
    best_score = node.weighted_sum
    best_move = random.choice(['w','a','s','d'])
    Q = col.deque()
    Q.append(node)
    while Q:
        visited_node = Q.pop()
        tree_count += 1
        # check if current score is greater than or equal to max score, if it is, update best score and node
        if (visited_node.weighted_sum) >= best_score:
            best_node = visited_node
            best_move = visited_node.move_path[0]
            best_score = visited_node.weighted_sum
        # enqueue children nodes
        if visited_node.up:
            Q.append(visited_node.up)
        if visited_node.right:
            Q.append(visited_node.right)
        if visited_node.left:
            Q.append(visited_node.left)
        if visited_node.down:
            Q.append(visited_node.down)
            
    return best_move
    
# return all four moves in descending order of frequency in the tree simulation results
def best_moves_descending(moves):
    c = col.Counter()
    for move in moves:
        c[move] += 1
    return c.most_common()
    