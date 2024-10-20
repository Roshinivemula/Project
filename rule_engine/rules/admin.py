from django.contrib import admin
from .models import Rule

# Define a custom admin interface for the Rule model
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rule_string', 'created_at', 'updated_at')
    search_fields = ('name', 'rule_string')
    ordering = ('-created_at',)

# Register the Rule model with the custom admin interface
admin.site.register(Rule, RuleAdmin)
