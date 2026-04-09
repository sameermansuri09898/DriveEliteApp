from rest_framework.routers import DefaultRouter
from product.views import CarList

router = DefaultRouter()
router.register('cars', CarList)

urlpatterns = router.urls