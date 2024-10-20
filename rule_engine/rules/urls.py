from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RuleViewSet, combine_rules, evaluate_rule,create_rule

router = DefaultRouter()
router.register(r'rules', RuleViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('create_rules/', create_rule, name='create_rules'),
    path('combine_rules/', combine_rules, name='combine_rules'),
    path('evaluate_rule/', evaluate_rule, name='evaluate_rule'),
]
