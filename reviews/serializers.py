from rest_framework import serializers
from .models import Review, ReviewHistory


class ReviewHistorySerializer(serializers.ModelSerializer):
    editor_username = serializers.CharField(
        source='editor.username', read_only=True)  # Show editor's username

    class Meta:
        model = ReviewHistory
        fields = ['id', 'review', 'editor', 'editor_username',
                  'edited_at', 'updated_feedback', 'revision_number']
        # Auto-set on creation
        read_only_fields = ['edited_at', 'revision_number']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(
        source='reviewer.username', read_only=True)  # Show reviewer's username
    review_history = ReviewHistorySerializer(
        many=True, read_only=True, source='history')  # Show all history revisions
    reviewer_avatar = serializers.ImageField(
        source='reviewer.profile.avatar', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'track', 'reviewer', 'reviewer_username',
                  'reviewer_avatar', 'comment', 'status', 'reviewed_at', 'review_history']
        read_only_fields = ['reviewed_at']
