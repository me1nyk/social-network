from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Profile, Like
from .serializers import PostSerializer, ProfileSerializer, LikeSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"success": True}
        return response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("user")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.action == "list":
            queryset = queryset.filter(is_published=True)
        elif self.action == "retrieve":
            queryset = queryset.filter(pk=self.kwargs.get("pk"))
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().select_related("user")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Profile.objects.all()
        if self.action == "list":
            queryset = queryset.filter(visibility="public")
            search_query = self.request.query_params.get("search", None)
            if search_query:
                queryset = queryset.filter(
                    Q(user__email__icontains=search_query)
                )
        elif self.action == "retrieve":
            queryset = queryset.filter(pk=self.kwargs.get("pk"))
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        follow = self.request.data.get("follow", None)
        if follow is not None and (self.request.method == "PATCH" or self.request.method == "PUT"):
            instance = serializer.instance
            user = self.request.user
            if follow:
                instance.followers.add(user)
            else:
                instance.followers.remove(user)
        serializer.save()


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get("post")

        existing_like = Like.objects.filter(user=user, post=post_id).first()

        if existing_like:
            return Response({"detail": "This post has already been liked."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data={"user": user.id, "post": post_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        like_id = kwargs.get("pk")

        like = Like.objects.filter(pk=like_id).first()

        if like:
            if like.user == request.user:
                like.delete()
                return Response({"detail": "Like has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You cannot delete this like because you are not the owner."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
