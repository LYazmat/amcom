from .views import ProductViewSet, CustomerViewSet, SellerViewSet, SaleViewSet, SellerCommissionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('customer', CustomerViewSet, basename='customer')
router.register('seller', SellerViewSet, basename='seller')
router.register('sale', SaleViewSet, basename='sale')
router.register('sellercommision', SellerCommissionViewSet,
                basename='commission')

urlpatterns = [
] + router.urls
