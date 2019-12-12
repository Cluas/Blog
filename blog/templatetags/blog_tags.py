from algoliasearch_django import get_adapter
from django import template
from django.conf import settings
from django.db.models.aggregates import Count

from blog.models import Post, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-publish")[:num]


@register.simple_tag
def archives():
    return Post.objects.dates("created", "month", order="DESC")


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count("post_category")).filter(
        num_posts__gt=0
    )


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count("post")).filter(num_posts__gt=0)


@register.simple_tag
def algolia():
    context = {
        "appID": settings.ALGOLIA["APPLICATION_ID"],
        "searchKey": settings.ALGOLIA["SEARCH_API_KEY"],
        "indexName": get_adapter(Post).index_name,
    }
    return context
