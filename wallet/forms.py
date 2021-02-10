from django import forms

from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'category', 'description', 'amount']
        labels = {
            'title': 'Название',
            'category': 'Категория',
            'description': 'Описание',
            'amount': 'Цена',
        }
        # help_texts = {
        #     'description': 'описание покупки'
        # }

        widgets = {
            'category': forms.Select(attrs={'id': 'choicewa', 'title': 'Your cat'}),
        }


class CategoryUpdateForm(forms.ModelForm):
    title = forms.CharField(label='Название')

    class Meta:
        model = Category
        fields = ['id', 'title']
