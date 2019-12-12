import algoliasearch_django as algoliaserach
from django.apps import AppConfig

from .index import PostIndex


class BlogConfig(AppConfig):
    name = "blog"

    def ready(self):
        post_model = self.get_model("post")
        algoliaserach.register(post_model, PostIndex)
