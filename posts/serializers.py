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
    is_public = serializers.BooleanField(default=True)  

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def validate_video(self, value):
        request = self.context.get('request')
        if request and request.method == 'POST':
            if value is None:
                return
            if not value.name.lower().endswith(('.mp4', '.avi', '.mov')):
                raise serializer.ValidationError("Only MP4,AVI, and MOV vedio files are allowed.")
            elif value.size > 50 * 1044 * 1024:
                raise serializer.ValidationError("Video size larger than 50MB!")  
        else:
            if value is None:
                return self.instance.video
            if not value.name.lower().endswith(('.mp4','avi','.mov')):
                raise serializer.ValidationError("Only MP4, AVI, and MOV video files are allowed.")
            elif value.size > 50 * 1024 * 1024:
                raise serializer.ValidationError('Video size is largaer than 50MB')
        return value     


    def validate(self, data): 
        print("data is validate method", data)
        # check if 'video' field is present in the data and has changed 
        # added not to trigger validate method since uploaded file was validated on Post
        # request and no need validating if instance is not chnaging
        if 'video' in data and self.instance and self.instance.video != data['video']:
            video = data.get(video)
            #Validate video filed
            self.validate_video(video)

        # Check if 'image' field is present in the data
        if 'image' in data:
            image = data.get('image')
            self.validate_image(image)

        return data                                    


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
            'title', 'content', 'image', 'video', 
            'like_id', 'likes_count', 'comments_count', 'is_public',
        ]