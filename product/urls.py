from rest_framework.routers import DefaultRouter
from product.views import CarList,carlist,RetrieveCarView,Carlistproto,AddtoCartView,CartView
from django.urls import path

router = DefaultRouter()
router.register('cars', CarList)

urlpatterns = router.urls
urlpatterns += [
    path('carslist/', carlist.as_view()),
    path('carsretreave/<int:pk>/', RetrieveCarView.as_view()),
    path('carslistproto/', Carlistproto.as_view()),
    path('add-to-cart/', AddtoCartView.as_view()),
    path('cart/', CartView.as_view()),
]