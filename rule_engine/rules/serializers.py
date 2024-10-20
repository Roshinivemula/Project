from rest_framework import serializers
from .models import Rule

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'rule_name', 'rule_ast', 'created_at', 'updated_at']
