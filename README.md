# Restaurant-Decision-Tree
This program provides a simple implementation of a decision tree that learns from a set of examples represented as RestaurantExample objects. The decision tree can then be used to determine whether one should wait at a restaurant based on several factors.

## Components
The primary components of this project are:

1. RestaurantExample: This is a class that represents a single example from the restaurant dataset. Each example encapsulates various attributes about the restaurant.
2. DecisionTree: This class implements the decision tree. It includes methods for training the tree based on a set of RestaurantExample objects and for printing the structure of the decision tree.

## Usage
To use the project, follow these steps:

1. Prepare a CSV file with restaurant examples. Each row in the CSV file should represent a single example and include the attributes mentioned above, in the same order.
2. Run the script from the command line with the CSV file as an argument:
```
python DecisionTree.py data.csv
```
The script will read the data, train the decision tree, and then print the decision tree structure to the console.
If you run the script without providing a CSV file, it will prompt you to enter the file name:
```
python DecisionTree.py
```
## Example Output

Here is an example of the output you can expect after running the script:

```
Please enter the input file name: data.csv
Patrons
├── Full
│   └── Hungry
│       ├── No => No
│       └── Yes
│           └── Food Type
│               ├── Italian => No
│               ├── Thai
│               │   └── Friday/Saturday
│               │       ├── No => No
│               │       └── Yes => Yes
│               ├── Burger => Yes
│               └── French => Yes
├── Some => Yes
└── None => No
```

This output represents the decision tree structure learned from the provided restaurant data. The tree branches represent the different choices or decisions at each node, and the leaves represent the final decision whether to wait or not.

