"""
Define the structure of CSU, CSP, MO
"""

from secure import param, prime, pseudo_random_generator, rand_num
from structure import Node


class ModelOwner():
    def __init__(self, model):
        self.seed = rand_num()
        self.model = model
        self.share1 = self.copy1(self.model, self.seed)
        self.share2 = self.copy2(self.model, self.share1)

    def copy1(self, original, seed):
        node = Node(None)
        node.attribute = original.attribute
        node.threshold = pseudo_random_generator(seed)

        if original.is_leaf_node:
            node.is_leaf_node = True
        else:
            binary = bin(node.threshold)[2:].zfill(param())
            first = int(binary[:param()//2], 2)
            second = int(binary[param()//2:], 2)

            node.left_child = self.copy1(original.left_child, first)
            node.right_child = self.copy1(original.right_child, second)
        return node

    def copy2(self, original, share1):
        node = Node(None)
        node.attribute = original.attribute
        node.threshold = (original.threshold - share1.threshold) % prime()

        if original.is_leaf_node:
            node.is_leaf_node = True
        else:
            node.left_child = self.copy2(
                original.left_child, share1.left_child)
            node.right_child = self.copy2(
                original.right_child, share1.right_child)
        return node

    def distributed_shares(self, csu, csp):
        csu.seed = self.seed
        csp.node = self.share2
        csu.generate_root()


class CloudServiceProvider():
    def __init__(self):
        self.node = None
        self.data = None


class CloudServiceUser():
    def __init__(self, data=None):
        self.data = data
        self.seed = None
        self.node = None
        if data is not None:
            self.split_data()

    def new_data(self, data):
        self.data = data
        self.split_data()

    def split_data(self):
        self.share1 = {key: rand_num() for key in self.data.keys()}
        self.share2 = {
            key: (self.data[key]-self.share1[key]) % prime() for key in self.data.keys()}

    def generate_root(self):
        self.node = Node(None)
        self.node.threshold = pseudo_random_generator(self.seed)

    def send_share(self, csp):
        csp.data = self.share2
