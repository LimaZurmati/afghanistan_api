from django.db.models import Count, Q
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from afghanistan_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
import cloudinary
import cloudinary.uploader

class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in.
    The perform_create method associates the post with the logged-in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).filter(
            Q(is_public=True) | Q(owner=user)  # Use Q objects for OR queries
        ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]

    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        request = self.request
        
        # Initialize placeholder for media URLs
        image_url = None
        video_url = None

        # Check if there's an image file in the request
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            # Upload the image to Cloudinary
            cloudinary_response = cloudinary.uploader.upload(image_file, resource_type='image')
            image_url = cloudinary_response.get('secure_url', None)

        # Check if there's a video file in the request
        if 'video' in request.FILES:
            video_file = request.FILES['video']
            # Upload the video to Cloudinary
            cloudinary_response = cloudinary.uploader.upload(video_file, resource_type='video')
            video_url = cloudinary_response.get('secure_url', None)

        # Save the post with the media URLs
        serializer.save(owner=request.user, image=image_url, video=video_url)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).order_by('-created_at')