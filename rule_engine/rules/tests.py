from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Rule
from .ast import Node
import json

class RuleEngineTests(TestCase):

    def setUp(self):
        # Create test data
        self.client = APIClient()
        
        # Sample rules to test
        self.rule_1 = {
            "name": "Age and Department Rule",
            "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        }
        
        self.rule_2 = {
            "name": "Marketing Rule",
            "rule_string": "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
        }

        # Add rules to the database
        self.client.post('/rules/api/', self.rule_1, format='json')
        self.client.post('/rules/api/', self.rule_2, format='json')

    def test_create_rule(self):
        # Test that a rule is created successfully
        response = self.client.post('/rules/api/', {
            "name": "Test Rule",
            "rule_string": "(age > 30 AND department = 'Sales')"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Test Rule")
        self.assertTrue('rule_string' in response.data)

    def test_combine_rules(self):
        # Combine rules and check response
        response = self.client.post('/rules/api/combine_rules/', {
            "rules": [
                "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
                "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
            ]
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('combined_ast' in response.data)

    def test_evaluate_rule(self):
        # Example of evaluating a rule
        ast = Node("operator", 
                   left=Node("operand", value="age > 30"), 
                   right=Node("operand", value="department = 'Sales'"))
        
        user_data = {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 3
        }
        
        response = self.client.post('/rules/api/evaluate_rule/', {
            "ast": ast,
            "user_data": user_data
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], True)

    def test_invalid_rule(self):
        # Test for invalid rule (missing operator)
        response = self.client.post('/rules/api/', {
            "name": "Invalid Rule",
            "rule_string": "age > 30 department = 'Sales'"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rule_evaluation_with_invalid_data(self):
        # Test for evaluating with missing user data
        ast = Node("operator", 
                   left=Node("operand", value="age > 30"), 
                   right=Node("operand", value="department = 'Sales'"))
        
        user_data = {
            "age": 25  # Missing department
        }

        response = self.client.post('/rules/api/evaluate_rule/', {
            "ast": ast,
            "user_data": user_data
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
