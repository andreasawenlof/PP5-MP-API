from rest_framework import serializers
from .models import Review, ReviewHistory
from tracks.models import Track


class ReviewHistorySerializer(serializers.ModelSerializer):
    editor_username = serializers.CharField(source="editor.username", read_only=True)
    revision_details = serializers.SerializerMethodField()

    class Meta:
        model = ReviewHistory
        fields = [
            "id",
            "review",
            "editor",
            "editor_username",
            "edited_at",
            "updated_feedback",
            "revision_details",
        ]
        read_only_fields = ["edited_at", "revision_details"]

    def get_revision_details(self, obj):
        request = self.context.get("request")
        if request and request.user.profile.is_composer:
            return {"number": obj.revision_number, "feedback": obj.updated_feedback}
        return {"feedback": obj.updated_feedback}


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(
        source="reviewer.username", read_only=True
    )
    reviewer_avatar = serializers.ImageField(
        source="reviewer.profile.avatar", read_only=True
    )

    # 🔥 Include track details
    track_title = serializers.CharField(source="track.title", read_only=True)
    track_status = serializers.CharField(source="track.status", read_only=True)
    track_genre = serializers.CharField(source="track.genre.name", read_only=True)
    track_mood = serializers.CharField(source="track.mood.name", read_only=True)
    track_project_type = serializers.CharField(
        source="track.project_type.name", read_only=True
    )

    review_history = ReviewHistorySerializer(
        many=True, read_only=True, source="history"
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "track",
            "track_title",
            "track_status",
            "track_genre",
            "track_mood",
            "track_project_type",
            "reviewer",
            "reviewer_username",
            "reviewer_avatar",
            "feedback",
            "status",
            "reviewed_at",
            "review_history",
        ]
        read_only_fields = ["reviewer", "reviewed_at", "status"]

    def validate_track(self, value):
        if value.status != "ready_for_review":
            raise serializers.ValidationError("This track is not ready for review.")
        return value
