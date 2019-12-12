from django.contrib.syndication.views import Feed

from blog.models import Post


class LatestPostsRssFeed(Feed):
    title = "Cluas's Blog "
    link = "/"
    description = "Cluas's Blog"

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return "[{}]{}".format(item.category, item.title)

    def item_description(self, item):
        return item.body
