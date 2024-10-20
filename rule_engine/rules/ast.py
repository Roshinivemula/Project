class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # "operator" or "operand"
        self.left = left  # Left child (if any)
        self.right = right  # Right child (if any, for operators)
        self.value = value  # Value for operand (e.g., number for comparison)
