from .views import ProductViewSet, CustomerViewSet, SellerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet, basename='ProductModel')
router.register('customer', CustomerViewSet, basename='CustomerModel')
router.register('seller', SellerViewSet, basename='SellerModel')

urlpatterns = [
] + router.urls
