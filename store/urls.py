from django.urls import path
from store import views
from .views import Login,products,Cart,Checkout,Orders
from store.middlewares.auth import auth_middleware

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', products.as_view(), name='products'),
    path('signup', views.signup, name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('orders', auth_middleware(Orders.as_view()), name='orders'),
]