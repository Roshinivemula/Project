import ast

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value,
        }

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        return Node(
            type=data['type'],
            left=Node.from_dict(data['left']),
            right=Node.from_dict(data['right']),
            value=data['value'],
        )

def create_rule(rule_string):
    # Use Python's `ast` library to parse the rule string and convert to custom AST
    try:
        tree = ast.parse(rule_string, mode='eval')
        return _build_ast_from_expr(tree.body).to_dict()
    except Exception as e:
        raise ValueError(f"Invalid rule string: {e}")

def _build_ast_from_expr(expr):
    if isinstance(expr, ast.BoolOp):
        op = 'AND' if isinstance(expr.op, ast.And) else 'OR'
        return Node(type="operator", left=_build_ast_from_expr(expr.values[0]), right=_build_ast_from_expr(expr.values[1]), value=op)
    elif isinstance(expr, ast.Compare):
        return Node(type="operand", value=f"{expr.left.id} {expr.ops[0].__class__.__name__} {expr.comparators[0].n}")
    else:
        raise ValueError(f"Unsupported expression: {expr}")

def combine_rules(rule_asts):
    if not rule_asts:
        raise ValueError("No rules provided")
    
    root = Node(type="operator", value="AND", left=Node.from_dict(rule_asts[0]))
    
    for rule_ast in rule_asts[1:]:
        new_node = Node(type="operator", value="AND", left=root, right=Node.from_dict(rule_ast))
        root = new_node
    
    return root.to_dict()

def evaluate_rule_ast(rule_ast, attributes):
    node = Node.from_dict(rule_ast)
    return _evaluate_node(node, attributes)

def _evaluate_node(node, attributes):
    if node.type == "operator":
        left_eval = _evaluate_node(node.left, attributes)
        right_eval = _evaluate_node(node.right, attributes)
        if node.value == "AND":
            return left_eval and right_eval
        elif node.value == "OR":
            return left_eval or right_eval
    elif node.type == "operand":
        return eval(node.value.format(**attributes))
    return False
