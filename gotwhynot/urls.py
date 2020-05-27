"""sputnikecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from shop import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', views.index,name='index'),
    path('shop/<int:id>/', views.detail,name='detail'),
    path('add-to-cart/(?P<id>[\w-]+)/$', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart,name='cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('remove-from-cart/(?P<id>/$', views.remove_from_cart, name="remove-from-cart"),
    path('update-quantity/(?P<id>/$', views.update_quantity, name="update-quantity"),
    path('', views.home, name='home'),
    path('checkout/charge', views.charge,name='charge'),
    path('orderconfirmation/', views.orderconfirmation,name='orderconfimration'),
    path('shop/champion/',views.champion,name='champion'),
    path('shop/yeezy/',views.yeezy,name='yeezy'),
    path('shop/offwhite/',views.offwhite,name='offwhite')
]

