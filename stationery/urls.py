from .views import ProductViewSet, CustomerViewSet, SellerViewSet, SaleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet, basename='ProductModel')
router.register('customer', CustomerViewSet, basename='CustomerModel')
router.register('seller', SellerViewSet, basename='SellerModel')
router.register('sale', SaleViewSet, basename='SaleModel')

urlpatterns = [
] + router.urls
