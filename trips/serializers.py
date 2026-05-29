import requests
from rest_framework import serializers
from .models import Travel, Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "travel", "external_id", "notes", "is_visited"]
        read_only_fields = ["travel"]

    def validate_external_id(self, value):
        url = f"https://api.artic.edu/api/v1/artworks/{value}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                raise serializers.ValidationError(f"External ID {value} is not valid.")
        except requests.RequestException:
            raise serializers.ValidationError(
                "Art institute API is currently unavailable. Please try again later."
            )
        return value


class TravelSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=True)

    class Meta:
        model = Travel
        fields = ["id", "name", "description", "start_date", "is_completed", "places"]

    def create(self, validated_data):
        places_data = self.context["request"].data.get("places", [])

        if places_data and (len(places_data) < 1 or len(places_data) > 10):
            raise serializers.ValidationError(
                "A project must contain between 1 and 10 places."
            )

        validated_data.pop("places", None)

        travel = Travel.objects.create(**validated_data)

        for place_data in places_data:
            place_serializer = PlaceSerializer(data=place_data)
            place_serializer.is_valid(raise_exception=True)
            place_serializer.save(travel=travel)

        travel.check_status()
        return travel
