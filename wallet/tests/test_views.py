from django.contrib.auth.models import User
from django.test import TestCase

from wallet.forms import ExpenseForm, CategoryUpdateForm
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

    def test_save_form(self):
        self.client.login(username='user', password='123')
        self.client.post('/expense/create/',
                         data={'title': 'Test1', 'category': 1, 'description': 'Описание', 'amount': 50})
        self.assertEqual(Expense.objects.count(), 2)

        new_expense = Expense.objects.last()
        self.assertEqual(new_expense.title, 'Test1')

    def test_redirect_after_POST(self):
        self.client.login(username='user', password='123')
        response = self.client.post('/expense/create/',
                         data={'title': 'Test1', 'category': 1, 'description': 'Описание', 'amount': 50})
        self.assertRedirects(response, '/')


class CategoryPageTest(TestCase):
    """Тест страницы категории"""

    def setUp(self) -> None:
        self.user = User.objects.create(username='user', email='jacob@ya.ru', password='123')
        self.user.set_password('123')
        self.user.save()
        self.category = Category.objects.create(title='Категория 1')
        self.expense = Expense.objects.create(title='Тест', category=self.category, user=self.user, description='Описание', amount=100)

    def test_uses_category_template(self):
        response = self.client.get(f'/category/{self.category.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/category_detail.html')

    def test_display_update_form(self):
        response = self.client.get(f'/category/{self.category.id}/')
        self.assertIsInstance(response.context['form'], CategoryUpdateForm)
        self.assertContains(response, 'value="Категория 1"')

    def test_save_form(self):
        self.client.post(f'/category/{self.category.id}/', data={'title': 'Категория 2'})
        category = Category.objects.get(pk=1)
        self.assertEqual(category.title, 'Категория 2')
        self.assertEqual(Category.objects.count(), 1)

    def test_redirect_after_post(self):
        response = self.client.post(f'/category/{self.category.id}/', data={'title': 'Категория 2'})
        self.assertRedirects(response, f'/category/{self.category.id}/')



