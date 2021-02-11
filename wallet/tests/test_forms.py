from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, Client

from wallet.forms import ExpenseForm
from wallet.models import Expense, Category


class ExpenseFormTest(TestCase):
    """Тест формы добавления покупок"""

    def test_form_renders(self):
        form = ExpenseForm()
        self.assertIn('Название:', form.as_p())

    def test_form_save(self):
        pass
        # user = User.objects.create_user(
        #     username='user', email='jacob@…', password='top_secret')
        # category = Category.objects.create(title='Категория 1')
        # expense = Expense.objects.create(title='Тест', category=category, user=user, description='Описание', amount=100)
