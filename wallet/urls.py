from django.urls import path

from wallet.views import CategoryList, CategoryDetail, ExpenseCreate, ExpenseUpdateView, AddToCart

urlpatterns = [
    path('', CategoryList.as_view(), name='home'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='cat_detail'),
    path('expense/create/', ExpenseCreate.as_view(), name='exp_create'),
    path('expense/<int:pk>/', ExpenseUpdateView.as_view(), name='exp_upd'),
    path('add-to-cart/<int:pk>/', AddToCart.as_view(), name='add'),
]