from django.db import models

class Rule(models.Model):
    name = models.CharField(max_length=100)
    rule_string = models.TextField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name
