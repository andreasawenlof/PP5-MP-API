from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'owner',
                  'display_name', 'bio', 'avatar', 'is_editor', 'is_reviewer', 'created_at', 'updated_at']

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
