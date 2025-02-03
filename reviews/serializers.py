from rest_framework import serializers
from .models import Review, ReviewHistory


class ReviewHistorySerializer(serializers.ModelSerializer):
    editor_username = serializers.CharField(
        source='editor.username', read_only=True
    )
    revision_number = serializers.SerializerMethodField()

    class Meta:
        model = ReviewHistory
        fields = ['id', 'review', 'editor', 'editor_username',
                  'edited_at', 'updated_feedback', 'revision_number']
        read_only_fields = ['edited_at', 'revision_number']

    def get_revision_number(self, obj):
        """
        Only composers (you & Ennio) can see revision numbers.
        """
        request = self.context.get('request')
        if request and request.user.profile.is_composer:
            return obj.revision_number
        return None  # Hide for non-composers


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(
        source='reviewer.username', read_only=True
    )
    review_history = ReviewHistorySerializer(
        many=True, read_only=True, source='history'
    )
    reviewer_avatar = serializers.ImageField(
        source='reviewer.profile.avatar', read_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'track', 'reviewer', 'reviewer_username',
                  'reviewer_avatar', 'feedback', 'status', 'reviewed_at', 'review_history']
        read_only_fields = ['reviewer', 'reviewed_at', 'status']
