from rest_framework import serializers
from .models import InstrumentCategory, Instrument


class InstrumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentCategory
        fields = ['id', 'name']  # Include the ID and name in the response


class InstrumentSerializer(serializers.ModelSerializer):
    categories = InstrumentCategorySerializer(
        many=True)  # Nest the categories serializer
    image = serializers.ImageField(required=False)  # Optional image field

    class Meta:
        model = Instrument
        fields = ['id', 'name', 'categories', 'image']
