from django.conf.urls import url

from blog import views
from blog.feeds import LatestPostsRssFeed

urlpatterns = [
    url(r"^archives/$", views.ArchivesView.as_view(), name="archives"),
    url(r"^(?P<pk>\d+)/$", views.PostDetailView.as_view(), name="post_detail"),
    url(r"^tags/$", views.post_tags, name="post_tags"),
    url(r"^tags/(?P<name>.+)/$", views.TagDetailView.as_view(), name="tag_detail"),
    url(r"^archives/$", views.ArchivesView.as_view(), name="archive"),
    url("^category/$", views.category_list, name="category_list"),
    url(
        r"^category/(?P<name>.+)/$",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^latest/rss/$", LatestPostsRssFeed(), name="rss"),
]
