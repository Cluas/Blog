from algoliasearch_django import AlgoliaIndex


class PostIndex(AlgoliaIndex):
    fields = (
        "title",
        "category",
        "body",
        "author",
        "publish",
        "created",
        "updated",
        "status",
        "summary",
        "tags",
        "views",
        "id",
    )
    # geo_field = ''
    settings = {
        "searchableAttributes": [
            "title",
            "category",
            "body",
            "author",
            "publish",
            "summary",
            "tags",
            "views",
            "id",
        ],
        "attributesForFaceting": ["title", "body"],
        "customRanking": ["desc(publish)"],
        "queryType": "prefixAll",
        "highlightPreTag": "<mark>",
        "highlightPostTag": "</mark>",
        "hitsPerPage": 15,
    }
    index_name = "post"
