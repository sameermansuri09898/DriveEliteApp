from rest_framework.routers import DefaultRouter
from product.views import CarList,RetrieveCarView,Carlistproto,AddtoCartView,CartView,Usercar,totalmoneybyuser,CreateOrderView

from django.urls import path

router = DefaultRouter()
router.register(r'cars', CarList,basename='cars')
router.register(r'cart', CartView, basename='cart')

urlpatterns = router.urls

urlpatterns += [
    path('usercar/', Usercar.as_view()),
    path('carsretreave/<int:pk>/', RetrieveCarView.as_view()),
    path('carslistproto/', Carlistproto.as_view()),
    path('add-to-cart/', AddtoCartView.as_view()),
    path('totalmoneybyuser/', totalmoneybyuser.as_view()),
    path('create-order/', CreateOrderView.as_view()),
    
    
]   