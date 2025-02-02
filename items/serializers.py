from rest_framework import serializers
from .models import Item
from users.serializers import UserSerializer  # Import UserSerializer from the users app
from django.utils import timezone
from datetime import timedelta


class ItemSerializer(serializers.ModelSerializer):
    # Adding the complete user object as a read-only field
    added_by = UserSerializer(source="user", read_only=True)

    # Format the created_at field to a more readable format like "X minutes ago"
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Item
        fields = "__all__"  # Include all Item fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Use timezone.now() instead of datetime.now() to get an offset-aware datetime
        created_at = instance.created_at
        now = timezone.now()

        time_diff = now - created_at
        seconds = time_diff.total_seconds()

        if seconds < 60:
            time_str = f"{int(seconds)} seconds ago"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = int(seconds // 86400)
            time_str = f"{days} day{'s' if days > 1 else ''} ago"

        representation["created_at"] = time_str
        return representation
