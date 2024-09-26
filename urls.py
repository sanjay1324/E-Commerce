from django.urls import path,include
from .views import register_user
from .views import change_password
from .views import LoginLog
from .views import add_product
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import AddProductView, ProductDetailView, UpdateProductView, delete_product,AllProductDetailsView,AddOrderPurchased,delete_orderPurchased,RetrieveAllOrderPurchased
from .views import ImageListCreate,ImageRetrieve,ImageUpdate,ImageDestroy


urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/change_password/',change_password, name='change_password'),
    path('api/login_user/',LoginLog, name='login_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/addproduct',add_product,name='add_product'),
    path('products/add/', AddProductView.as_view(), name='add-product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/update/<int:pk>/', UpdateProductView.as_view(), name='update-product'),
    path('products/delete/<int:pk>/', delete_product, name='delete-product'),
    path('products/', AllProductDetailsView.as_view(), name='product-detail'),
    path('order-details/', AddOrderPurchased.as_view(), name='order-detail'),
    path('products/delete/<int:pk>/', delete_orderPurchased, name='delete-orderPurchased'),
    path('retrieve-orders/', RetrieveAllOrderPurchased.as_view(), name='order-detail'),
    path('images/', ImageListCreate.as_view(), name='image-list-create'),
    path('images/retrieve/<int:pk>/', ImageRetrieve.as_view(), name='image-retrieve'),
    path('images/update/<int:pk>/', ImageUpdate.as_view(), name='image-Update'),
    path('images/delete/<int:pk>/', ImageDestroy.as_view(), name='image-Delete'),

]