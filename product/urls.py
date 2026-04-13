from rest_framework.routers import DefaultRouter
from product.views import CarList,carlist,RetrieveCarView,Carlistproto
from django.urls import path

router = DefaultRouter()
router.register('cars', CarList)

urlpatterns = router.urls
urlpatterns += [
    path('carslist/', carlist.as_view()),
    path('carsretreave/<int:pk>/', RetrieveCarView.as_view()),
    path('carslistproto/', Carlistproto.as_view()),
]