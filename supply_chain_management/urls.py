"""supply_chain_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from scm import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home_view'),
    path('postlogin', views.post_login_view,name='postlogin'),
    path('user/', include('user.urls')),
    path('supplier/', include('scm.supplier_urls')),
    path('product/', include('scm.product_urls')),
    path('purchaseorder/',include('scm.order_urls')),
    path("reports", views.reports_view, name="reports_dashboard"),
    path('grn-inward', views.grn_inward_view,name='grn_inward'),
    path('trigger-grn-inward', views.trigger_grn_inward_view,name='trigger_grn_lambda'),
    path('inventory', views.auto_generate_purchase_orders,name='auto_generate_purchase_orders'),
    path('logout', LogoutView.as_view(template_name='home/base.html'),name='logout'),

]
