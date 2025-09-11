from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.permissions import AllowAny

from app.models import Blog, Comment
from app.serializer import BlogSerializer, CommentSerializer
from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')
    return render(request, "detail.html", {"blog": blog, "comments": comments})


def home(request):
    return render(request, "index.html")

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Comment.objects.none()

        blog_id = self.kwargs.get("blog_pk")
        return Comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs.get("blog_pk")
        serializer.save(blog_id=blog_id)

