"""
Define the structure of Node, Timer
"""
import time


class Node():
    def __init__(self, data):
        self.data = data
        self.attribute = None
        self.threshold = None
        self.left_child = None
        self.right_child = None
        self.is_leaf_node = False


class Timer():
    def __init__(self, detail=None):
        self.start_time = time.time()
        self.detail = detail

    def reset(self, detail=None):
        self.start_time = time.time()
        self.detail = detail

    def end(self, detail=None):
        if detail is not None:
            self.detail = detail
        interval = (time.time() - self.start_time) * 1000
        #print(f"{self.detail}共花費 {interval:.4f}豪秒")
        return interval
