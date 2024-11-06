from rest_framework import serializers
from posts.models import Post
from likes.models import Like
from PIL import Image as PilImage
import io

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_public = serializers.BooleanField(default=True)  # Include is_public

    # Validate image uploads
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  # Limit to 2MB
            raise serializers.ValidationError('Image size larger than 2MB!')
        
        # Open the image using Pillow to get dimensions
        image = PilImage.open(value)
        width, height = image.size
        
        if height > 4096:  # Limit height
            raise serializers.ValidationError('Image height larger than 4096px!')
        if width > 4096:  # Limit width
            raise serializers.ValidationError('Image width larger than 4096px!')
        
        return value

    # Validate video uploads
    def validate_video(self, value):
        if value.size > 10 * 1024 * 1024:  # Limit to 10MB
            raise serializers.ValidationError('Video size larger than 10MB!')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'video',  # Added video field
            'like_id', 'likes_count', 'comments_count', 'is_public',
        ]