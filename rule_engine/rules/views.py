from rest_framework import viewsets, serializers
from .models import Rule
from .ast import Node
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Rule Serializer
class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'name', 'rule_string', 'description']

# Rule ViewSet
class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

@api_view(['POST'])
def create_rule(request):
    rule_string = request.data.get('rule_string', '')

    if not rule_string:
        return Response({"error": "Rule string is required"}, status=400)
    
    # This is a simplified approach for parsing, needs more sophisticated parsing in real applications
    try:
        # Split by operators (AND/OR) for a basic example
        # Example: rule_string = "age > 30 AND department = 'Sales'"
        if 'AND' in rule_string:
            operator = "AND"
            left_expr, right_expr = rule_string.split('AND', 1)
        elif 'OR' in rule_string:
            operator = "OR"
            left_expr, right_expr = rule_string.split('OR', 1)
        else:
            operator = "AND"  # Default to AND if no operator is found
            left_expr = rule_string
            right_expr = ''

        # Clean up spaces
        left_expr = left_expr.strip()
        right_expr = right_expr.strip()

        # Creating the AST for this rule string
        left_node = Node(type="operand", value=left_expr)
        right_node = Node(type="operand", value=right_expr)
        ast_node = Node(type="operator", value=operator, left=left_node, right=right_node)

        # Return AST as a string or in any format you prefer
        return Response({
            "ast": {
                "type": ast_node.type,
                "value": ast_node.value,
                "left": {
                    "value": ast_node.left.value
                },
                "right": {
                    "value": ast_node.right.value
                }
            }
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)

# Combine rules logic
@api_view(['POST'])
def combine_rules(request):
    rules = request.data.get('rules', [])
    combined_ast = None
    for rule in rules:
        ast = create_rule(rule)
        if combined_ast is None:
            combined_ast = ast
        else:
            # Combine the current rule AST with the existing one using AND/OR logic
            combined_ast = Node(type="operator", left=combined_ast, right=ast)
    return Response({"combined_ast": str(combined_ast)})

# Evaluate rule logic
@api_view(['POST'])
def evaluate_rule(request):
    ast = request.data.get('ast')
    user_data = request.data.get('user_data', {})
    
    # Implement AST evaluation logic here
    def evaluate_node(node, user_data):
        if node.type == "operand":
            # Example: Check if user data satisfies the condition in the node
            if node.value == "age > 30":
                return user_data["age"] > 30
            # Other conditions can be handled similarly
        elif node.type == "operator":
            left_result = evaluate_node(node.left, user_data)
            right_result = evaluate_node(node.right, user_data)
            if node.value == "AND":
                return left_result and right_result
            elif node.value == "OR":
                return left_result or right_result
        return False
    
    result = evaluate_node(ast, user_data)
    return Response({"result": result})
