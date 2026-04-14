from rest_framework import viewsets
from product.models import Car,CarImage
from product.productserializer import CarSerializer,CarImageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from product.productserializer import BookingSerializer

class CarList(viewsets.ModelViewSet):

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    # ✅ CREATE
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.save()

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

class carlist(APIView):
    permission_classes = [IsAuthenticated]
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

class BookingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self,request):
        print(request.data)
        serializer=BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            car=Car.objects.get(id=request.data['car'])
            car.is_available=False
            car.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
