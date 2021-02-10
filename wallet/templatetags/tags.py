from django import template
from django.db.models import Sum, F

from wallet.models import Expense

register = template.Library()


@register.simple_tag
def sum_all_expense_in_category(pk):
    return Expense.objects.filter(category=pk).aggregate(cou=Sum(F('amount')+1))


@register.inclusion_tag('wallet/tags/tmp_tag_form_add_expense.html', takes_context=True)
def edit_form_tag(context):
    return context