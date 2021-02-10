from django.contrib.auth.models import User
from django.test import TestCase

from wallet.forms import ExpenseForm
from wallet.models import Category, Expense


class HomePageTest(TestCase):
    """Тест главной страницы"""

    def setUp(self) -> None:
        user = User.objects.create(username='user', email='jacob@ya.ru', password='123')
        user.set_password('123')
        user.save()
        category = Category.objects.create(title='Категория 1')
        expense = Expense.objects.create(title='Тест', category=category, user=user, description='Описание', amount=100)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/index.html')

    def test_uses_form_create_expense(self):
        """Тест, что на главной есть форма"""
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ExpenseForm)

    def test_send_form(self):
        self.client.login(username='user', password='123')
        self.client.post('/expense/create/',
                         data={'title': 'Test1', 'category': 1, 'description': 'Описание', 'amount': 50})
        self.assertEqual(Expense.objects.count(), 2)

        new_expense = Expense.objects.last()
        self.assertEqual(new_expense.title, 'Test1')



