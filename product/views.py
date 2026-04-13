from rest_framework import viewsets
from product.models import Car,CarImage
from product.productserializer import CarSerializer,CarImageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

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

class carlist(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class Carlistproto(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.order_by('-id')[:8]


class RetrieveCarView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer