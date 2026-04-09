from rest_framework import viewsets
from product.models import Car,CarImage
from product.productserializer import CarSerializer,CarImageSerializer
from rest_framework.response import Response
from rest_framework import status

class CarList(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.save()

        
        for img in images:
            CarImage.objects.create(car=car, image=img)

        return Response(self.get_serializer(car).data, status=status.HTTP_201_CREATED)