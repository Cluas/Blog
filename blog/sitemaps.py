from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    """文章站点地图"""

    change_freq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def last_mod(self, obj):
        return obj.publish
