"""cluas_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from blog.sitemaps import PostSitemap
from blog.views import IndexView

sitemaps = {"posts": PostSitemap}


urlpatterns = [
    url(r"^notifications/", include("notifications.urls", namespace="notifications")),
    url(r"^$", IndexView.as_view()),
    url(r"^admin/", admin.site.urls),
    url(r"^blog/", include("blog.urls", namespace="blog")),
    url(r"^accounts/", include("allauth.urls")),
    url(r"", include("ckeditor_uploader.urls")),
    url(r"", include("easy_comment.urls")),
    # url(r'', include('comments.urls', namespace='comments')),
    url(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG or True:
    urlpatterns += staticfiles_urlpatterns()
