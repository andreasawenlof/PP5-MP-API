from rest_framework import serializers
from .models import InstrumentCategory, Instrument


class InstrumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentCategory
        fields = ["id", "name"]  # Include the ID and name in the response


class InstrumentSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        queryset=InstrumentCategory.objects.all(),
        slug_field="name",
        many=True,
        required=False,  # ✅ Now optional
    )

    class Meta:
        model = Instrument
        fields = ["id", "name", "categories", "image"]

    def create(self, validated_data):
        """Assign 'No Category Yet' by default if none is provided."""
        category_names = validated_data.pop("categories", [])

        # ✅ Get or create the default 'No Category Yet'
        if not category_names:
            default_category, _ = InstrumentCategory.objects.get_or_create(
                name="No Category"
            )
            category_names = [default_category.name]

        # ✅ Create the instrument
        instrument = Instrument.objects.create(**validated_data)

        # ✅ Assign categories
        for name in category_names:
            category, _ = InstrumentCategory.objects.get_or_create(name=name)
            instrument.categories.add(category)

        return instrument
