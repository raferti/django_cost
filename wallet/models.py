from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    """Категории затрат"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('cat_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Expense(models.Model):
    """Затраты"""
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Затрата'
        verbose_name_plural = 'Затраты'

    def get_absolute_url(self):
        return reverse('exp_upd', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title} amount: {self.amount}'



