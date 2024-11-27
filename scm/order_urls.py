from django.urls import path
from . import views

urlpatterns = [
   path('list', views.purchase_order_list, name='purchase_order_list'),
   path('create', views.purchase_order_create, name="purchase_order_create"),
   path('update/<int:pk>', views.purchase_order_update, name="purchase_order_update"),
   path('delete/<int:pk>', views.purchase_order_delete, name="purchase_order_delete"),

]