from django.urls import path
from .views import posts,post_details,IndexPageView,AllPostsView,PostDetailView,ReadLaterView
urlpatterns = [
    # path("",index,name="home"),
    path("",IndexPageView.as_view(),name="home"),
    # path("posts",posts,name="posts"),
    path("posts",AllPostsView.as_view(),name="posts"),
    # path("posts/<int:id>",post_details,name="post-detail")
    path("posts/<int:id>",PostDetailView.as_view(),name="post-detail"),
    path("read-later",ReadLaterView.as_view(),name="read-later")
]