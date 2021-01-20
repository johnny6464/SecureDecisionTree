"""
1. Determine the size of the object
2. Determine the number of nodes of the tree
3. Perform the main protocol of evaluation
"""
import pickle
import sys
import time
from structure import Node
from secure import param, prime, pseudo_random_generator, rand_num

NODES = 0
DEPTH = 0


def size(obj):
    temp_obj = pickle.dumps(obj)
    return sys.getsizeof(temp_obj)


def tree_info(root):
    global NODES
    NODES = 0
    dfs(root, 0)
    return NODES, DEPTH


def dfs(current, depth):
    global NODES, DEPTH
    NODES += 1
    if current.is_leaf_node:
        if DEPTH < depth:
            DEPTH = depth
    else:
        dfs(current.left_child, depth + 1)
        dfs(current.right_child, depth + 1)


def secure_comparison(csu, csp, u_node, p_node):
    time.sleep(0.01)
    attribute = p_node.attribute

    x1 = csu.share1[attribute]
    y1 = u_node.threshold

    x2 = csp.data[attribute]
    y2 = p_node.threshold

    alpha = rand_num()
    a1 = rand_num()
    a2 = (alpha - a1) % prime()

    s1 = x1 + a1
    h1 = y1 + a1

    s2 = x2 + a2
    h2 = y2 + a2
    if (s1+s2) % prime() <= (h1+h2) % prime():
        return 0
    return 1


def child(current, left):
    binary = bin(current.threshold)[2:].zfill(param())
    first = int(binary[:param()//2], 2)
    second = int(binary[param()//2:], 2)

    node = Node(None)
    if left:
        node.threshold = pseudo_random_generator(first)
    else:
        node.threshold = pseudo_random_generator(second)
    return node


def protocol(csu, csp, u_node, p_node):
    while True:
        if p_node.is_leaf_node:
            return (u_node.threshold + p_node.threshold) % prime()
        if secure_comparison(csu, csp, u_node, p_node) == 0:
            p_node = p_node.left_child
            u_node = child(u_node, True)
        else:
            p_node = p_node.right_child
            u_node = child(u_node, False)
