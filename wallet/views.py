from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q, F, Prefetch, Case, When, Value as V, CharField
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from wallet.forms import ExpenseForm, CategoryUpdateForm
from wallet.models import Category, Expense


class CategoryList(ListView):
    template_name = 'wallet/index.html'
    queryset = Category.objects.prefetch_related('expenses').filter(expenses__user_id=1).annotate(cou=Count('expenses'))
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #total = Category.objects.filter(expenses__user=1).aggregate(total=Count('expenses'))
        #context['total'] = total
        context['form'] = ExpenseForm()
        return context


class CategoryDetail(UpdateView):
    template_name = 'wallet/category_detail.html'
    context_object_name = 'category'
    form_class = CategoryUpdateForm
    model = Category
    success_url = '/'

    def get_success_url(self):
        return reverse('cat_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        self.category = Category.objects.prefetch_related('expenses').get(pk=self.kwargs['pk'])
        return self.category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['total'] = Expense.objects.filter(category=self.kwargs['pk']).aggregate(cou=Sum(F('amount')+1))
        context['form'] = CategoryUpdateForm(instance=self.category)
        return context


class ExpenseCreate(CreateView):
    form_class = ExpenseForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            category = form.save(commit=False)
            category.user = self.request.user
            category.save()
        return redirect('home')


class ExpenseUpdateView(UpdateView):
    """Обновление покупки"""
    model = Expense
    fields = ('title', 'category', 'description', 'amount')
    context_object_name = 'expense'
    template_name = 'wallet/expense_detail.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ExpenseUpdateView, self).get_context_data(**kwargs)
        if pk := self.request.session.get('prod_id', ''):
            exp = Expense.objects.filter(pk__in=pk)
            context['goods'] = exp
        return context

    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        return redirect('home')


class AddToCart(View):
    def get(self, *args, **kwargs):
        #del self.request.session['prod_id']
        if 'prod_id' not in self.request.session:
            self.request.session['prod_id'] = []
        self.request.session['prod_id'].append(self.kwargs['pk'])
        self.request.session.modified = True

        return redirect('exp_upd', self.kwargs['pk'])







