from rest_framework import generics, permissions, filters
from afghanistan_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializer
from django.db.models import Count
from .models import Post


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    # for SearchFilter
    search_fields = [
        'owner__username',
        'content'
    ]
    # for DjangoFilterBackend
    filterset_fields = [
        # filter posts from followers
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile'
    ]
    # for OrderingFilter
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')