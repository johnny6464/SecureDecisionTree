"""
Implement the decision tree training, evaluation
"""

import math

from structure import Node


def find_best_attribute(data):
    min_entropy = 10
    best_attribute = None
    best_threshold = None
    for attribute in data.columns:
        for value in data.groupby(by=attribute).groups.keys():
            if attribute != 'label':
                entropy = compute_entropy(data, attribute, value)
                if entropy < min_entropy:
                    min_entropy = entropy
                    best_attribute = attribute
                    best_threshold = value
    return best_attribute, best_threshold


def compute_entropy(data, attribute, threshold):
    total_num = len(data)

    less_data = data[data[attribute] <= threshold]
    less_entropy = 0

    for label in less_data.groupby(by='label').groups.keys():
        proportion = len(less_data[less_data.label == label]) / len(less_data)
        less_entropy -= proportion * math.log2(proportion)

    great_data = data[data[attribute] > threshold]
    great_entropy = 0

    for label in great_data.groupby(by='label').groups.keys():
        proportion = len(
            great_data[great_data.label == label]) / len(great_data)
        great_entropy -= proportion * math.log2(proportion)

    return (len(less_data) / total_num) * less_entropy + (len(great_data) / total_num) * great_entropy


def is_all_same(data):
    for i in range(len(data)-1):
        if not (data.loc[i] == data.loc[i+1]).all():
            return False
    return True


def max_size(data):
    largest = 0
    max_label = 0
    for label, size in enumerate(data.groupby(by='label').size()):
        if size > largest:
            largest = size
            max_label = label+1
    return max_label


def build_tree(data, depth):
    data.reset_index(drop=True, inplace=True)
    node = Node(data)

    if depth == 14 or len(data) < 100 or is_all_same(data):
        node.is_leaf_node = True
        node.threshold = max_size(data)
        return node

    if len(data.groupby(by='label').groups.keys()) == 1:
        node.is_leaf_node = True
        node.threshold = data['label'][0]
        return node

    node.attribute, node.threshold = find_best_attribute(data)
    node.left_child = build_tree(
        data[data[node.attribute] <= node.threshold], depth + 1)
    node.right_child = build_tree(
        data[data[node.attribute] > node.threshold], depth + 1)
    return node


def training(data):
    print("Start training...")
    return build_tree(data, 0)


def predict(root, data):
    while not root.is_leaf_node:
        if data[root.attribute] <= root.threshold:
            root = root.left_child
        else:
            root = root.right_child
    return root.threshold


def evaluation(root, data):
    print("Start evaluation...")
    data.reset_index(drop=True, inplace=True)
    total = len(data)
    correct = 0

    for i in range(total):
        prediction = predict(root, data.loc[i])
        if prediction == data.loc[i]['label']:
            correct += 1

    print(f"Accuracy: {correct/total:.4f}")
