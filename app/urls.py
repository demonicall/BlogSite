from django.urls import include, path
from rest_framework.routers import DefaultRouter
from app.views import BlogView, CommentView, home, blog_detail
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'', BlogView)

blogs_router = routers.NestedDefaultRouter(router, r'', lookup='blog')
blogs_router.register(r'comments', CommentView, basename='blog-comments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(blogs_router.urls)),
    path('', home, name='home'),
    path('<int:pk>/detail/', blog_detail, name="blog-detail"),
]