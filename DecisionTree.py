
import csv
import sys
import math
from anytree import Node, RenderTree
from random import choice
from collections import Counter
from typing import List, Tuple


class RestaurantExample:
    def __init__(self, attributes_list):
        self.altitude = attributes_list[0]
        for i in range(1, 11):
            attributes_list[i] = attributes_list[i].lstrip()

        self.bar = attributes_list[1]
        self.fri = attributes_list[2]
        self.hungry = attributes_list[3]
        self.patrons = attributes_list[4]
        self.price = attributes_list[5]
        self.rain = attributes_list[6]
        self.reservation = attributes_list[7]
        self.food_type = attributes_list[8]
        self.estimated_waiting = attributes_list[9]
        self.wait_decision = attributes_list[10]

    def get_attribute(self, attribute):
        return getattr(self, attribute)

    def get_wait_decision(self):
        return self.wait_decision

class DecisionTree:
    def __init__(self, attributes: List[str], examples: List[RestaurantExample]):
        self.attributes = attributes
        self.examples = examples
        self.decision_tree = None

    def binary_entropy(self, probability: float) -> float:
        if probability == 0 or probability == 1:  # Edge case to avoid log(0)
            return 0
        return -(probability * math.log2(probability) + (1 - probability) * math.log2(1 - probability))


    def count_decisions(self, examples: List[RestaurantExample]) -> Tuple[int, int]:
        count_yes = sum(1 for example in examples if example.get_wait_decision() == 'Yes')
        count_no = len(examples) - count_yes
        return count_yes, count_no

    def majority_value(self, examples: List[RestaurantExample]) -> str:
        count_yes, count_no = self.count_decisions(examples)
        return choice(['retYes', 'retNo']) if count_yes == count_no else ('retYes' if count_yes > count_no else 'retNo')

    def has_same_decision(self, examples: List[RestaurantExample]) -> str:
        count_yes, count_no = self.count_decisions(examples)
        return 'Neither' if count_yes * count_no != 0 else ('Yes' if count_yes > 0 else 'No')

    def gain(self, attribute: str, examples: List[RestaurantExample]) -> float:
        value_decision_pairs = [(example.get_attribute(attribute), example.get_wait_decision()) for example in examples]
    
        value_decision_counter = Counter(value_decision_pairs)
        value_counter = Counter(example.get_attribute(attribute) for example in examples)
    
        entropy_sum = 0
        for value, decision in value_decision_counter:
            total = value_counter[value]
            prob = value_decision_counter[(value, decision)] / total
            if 0 < prob < 1:
                entropy_sum += (total / len(examples)) * self.binary_entropy(prob)
    
        return 1 - entropy_sum

    def unique_values(self, attribute: str, examples: List[RestaurantExample]) -> List[str]:
        return list(set(example.get_attribute(attribute) for example in examples))

    def decision_tree_learning(self, examples: List[RestaurantExample], attributes: List[str], parent_examples: List[RestaurantExample], parent_node: Node, all_examples: List[RestaurantExample]) -> Tuple[str, Node]:
        attribute_print_names = {'altitude': 'Altitude', 'bar': 'Bar', 'fri': 'Friday/Saturday', 'hungry': 'Hungry', 'patrons': 'Patrons','price': 'Price', 'rain': 'Rain', 'reservation': 'Reservation', 'food_type': 'Food Type', 'estimated_waiting': 'Estimated Waiting'}
        if not examples:
            return self.majority_value(parent_examples), parent_node
        elif (decision := self.has_same_decision(examples)) != 'Neither':
            return f'ret{decision}', parent_node
        elif not attributes:
            return self.majority_value(examples), parent_node
        else:
            best_attribute = max(attributes, key=lambda a: self.gain(a, examples))

            # Use the dictionary to get the print name
            best_attribute_print_name = attribute_print_names[best_attribute]

            if parent_node.name == 'Top':
                start_node = Node(best_attribute_print_name)
            else:
                start_node = Node(best_attribute_print_name, parent=parent_node)
        
    
            for value in self.unique_values(best_attribute, all_examples):
                child_node = Node(value, parent=start_node)
                new_examples = [example for example in examples if
                                example.get_attribute(best_attribute) == value]
                new_attributes = [attr for attr in attributes if attr != best_attribute]
                subtree = self.decision_tree_learning(new_examples, new_attributes, examples, child_node, all_examples)
                if subtree[0] == 'retYes':
                    child_node.name = f"{value} => Yes"
                elif subtree[0] == 'retNo':
                    child_node.name = f"{value} => No"
    
            return best_attribute, start_node


    def learn(self):
        pass_node = Node('Top')
        self.decision_tree = self.decision_tree_learning(self.examples, self.attributes, self.examples, pass_node, self.examples)
        return self.decision_tree

    def print_tree(self):
        for pre, fill, node in RenderTree(self.decision_tree[1]):
            print(f"{pre}{node.name}")


def read_data(input_file: str) -> List[RestaurantExample]:
    examples = []
    with open(input_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            examples.append(RestaurantExample(row))
    return examples


def main():
    if len(sys.argv) < 2:
        input_file = input("Please enter the input file name: ")
    else:
        input_file = sys.argv[1]

    examples = read_data(input_file)

    attributes = ['altitude', 'bar', 'fri', 'hungry', 'patrons', 'price', 'rain', 'reservation', 'food_type', 'estimated_waiting']

    decision_tree = DecisionTree(attributes, examples)
    decision_tree.learn()
    decision_tree.print_tree()

if __name__ == "__main__":
    main()


