from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Travel, Place
from .serializers import TravelSerializer, PlaceSerializer


# Create your views here.
class TravelViewSet(viewsets.ModelViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.places.filter(is_visited=True).exists():
            return Response(
                {"error": "Cannot delete a travel with visited places."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def create(self, request, *args, **kwargs):
        travel_id = request.data.get("travel")
        if not travel_id:
            return Response(
                {"error": "Travel ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            travel = Travel.objects.get(id=travel_id)
        except Travel.DoesNotExist:
            return Response(
                {"error": "Travel not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if travel.places.count() >= 10:
            return Response(
                {"error": "A travel cannot have more than 10 places."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        place = serializer.save(travel=travel)

        travel.check_status()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        place = serializer.save()
        place.travel.check_status()
