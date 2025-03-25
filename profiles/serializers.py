from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    avatar = serializers.ImageField(required=False)
    is_composer = serializers.BooleanField(read_only=True)  # Users can't edit this
    is_reviewer = serializers.BooleanField(read_only=True)  # Users can't edit this

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "display_name",
            "bio",
            "avatar",
            "is_composer",
            "is_reviewer",
            "created_at",
            "updated_at",
        ]

    def validate_display_name(self, value):
        """
        Prevents blank display names.
        """
        return value.strip() if value else self.instance.owner.username

    def to_representation(self, instance):
        """
        Ensures the avatar **always returns a URL** even if Cloudinary is missing.
        """
        data = super().to_representation(instance)
        if not instance.avatar:
            data["avatar"] = (
                "https://res.cloudinary.com/YOUR_CLOUDINARY_NAME/image/upload/DEFAULT_IMAGE_ID.jpg"
            )
        return data
