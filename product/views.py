from rest_framework import viewsets
from product.models import Car,CarImage,CarCart
from product.productserializer import CarSerializer,CarImageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from product.productserializer import CartSerializer
from rest_framework.decorators import action
import razorpay
from django.conf import settings
from product.models import Payment

class CarList(viewsets.ModelViewSet):
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    # ✅ CREATE
    def create(self, request, *args, **kwargs):
     images = request.FILES.getlist('images')

     serializer = self.get_serializer(data=request.data)
     serializer.is_valid(raise_exception=True)

    # 🔥 FIX: user assign karo
     car = serializer.save()
     car.user = request.user
     car.save()

     for img in images:
         CarImage.objects.create(car=car, image=img)

     return Response(self.get_serializer(car).data, status=status.HTTP_201_CREATED)

    # ✅ UPDATE (PUT)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        images = request.FILES.getlist('images')

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.save()

        if images:
            car.images.all().delete()
            for img in images:
                CarImage.objects.create(car=car, image=img)

        return Response(self.get_serializer(car).data, status=status.HTTP_200_OK)

    # ✅ PARTIAL UPDATE (PATCH)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        images = request.FILES.getlist('images')

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        car = serializer.save()

        if images:
            car.images.all().delete()
            for img in images:
                CarImage.objects.create(car=car, image=img)

        return Response(self.get_serializer(car).data, status=status.HTTP_200_OK)

    # ✅ DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()   
        return Response(status=status.HTTP_204_NO_CONTENT)

class Usercar(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        car=Car.objects.filter(user=request.user)
        serializer=CarSerializer(car,many=True)
        return Response(serializer.data)


class Carlistproto(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.order_by('-id')[:9]


class RetrieveCarView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class AddtoCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        car_id = request.data.get('car')
        days = int(request.data.get('days', 1))

        # ❌ invalid days
        if days < 1:
            return Response({"error": "Invalid days"}, status=400)

        # ✅ car exist check
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        if not car.is_available:
            return Response({"error": "Car not available"}, status=400)

        price_per_day = car.perday_offer_price()
        total_price = price_per_day * days

        
        item, created = CarCart.objects.get_or_create(
            user=request.user,
            car=car,
            defaults={
                'days': days,
                'total_price': total_price
            }
        )

        if not created:
            item.days = days
            item.total_price = price_per_day * item.days
            item.save()

            return Response({
                "message": "Cart updated",
                "days": item.days,
                "total_price": item.total_price
            }, status=200)

        return Response({
            "message": "Car added to cart",
            "days": item.days,
            "total_price": item.total_price
        }, status=201)


class CartView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        cart = CarCart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    def destroy(self,request,pk=None):
        try:
            cart=CarCart.objects.get(id=pk)
            cart.delete()
            return Response({"message": "Car removed from cart"}, status=200)
        except CarCart.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

    def update(self,request,pk=None):
        try:
            cart=CarCart.objects.get(id=pk,user=request.user)
            days=request.data.get('days')

            try:
             if days < 1:
                 return Response({"error": "Invalid days"}, status=400)

            except ValueError:
                return Response({"error": "Invalid days"}, status=400)

            cart.days=int(days)    
            cart.total_price=cart.car.perday_offer_price()*cart.days
            cart.save()
            return Response({
            "message": "Cart updated successfully",
            "days": cart.days,
            "total_price": cart.total_price
            }, status=200)  

        except CarCart.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)        

class totalmoneybyuser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        cart=CarCart.objects.filter(user=request.user)
        total_price=0
        for item in cart:
            total_price+=item.total_price
        print(total_price)    
        return Response({"total_price": total_price})


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        cart_items = CarCart.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)

        if total_price <= 0:
            return Response({"error": "Cart is empty"}, status=400)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            order = client.order.create({
                "amount": int(total_price * 100),  # paise
                "currency": "INR",
                "payment_capture": 1,
                "receipt": f"order_rcptid_{request.user.id}",
                "notes": {
                    "user_id": request.user.id
                }
            })
            print("Razorpay Order:", order)  # check terminal

        except Exception as e:
            print("Razorpay Error:", str(e))  # ✅ see exact error
            return Response({"error": str(e)}, status=500)

        Payment.objects.create(
            user=request.user,
            Razorpay_order_id=order['id'],
            total_price=total_price,
            status="created"
        )

        return Response({
         "id": order['id'],
         "amount": order['amount'],
         "currency": order['currency']
})
