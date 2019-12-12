import markdown
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension

from blog.models import Post, Category, Tag


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)  # 获取当前context内容
        paginator = context.get("paginator")
        page = context.get("page_obj")
        is_paginated = context.get("is_paginated")
        pagination_data = self.pagination_data(paginator, page, is_paginated)  # 获取分页数据
        context.update(pagination_data)
        return context

    def get_queryset(self):
        posts = super(IndexView, self).get_queryset().filter(status="2")
        return posts

    @staticmethod
    def pagination_data(paginator, page, is_paginated):
        """获取自己需要的分页数据"""
        if not is_paginated:
            return {}  # 如果没有分页。则无需显示分页导航栏
        # 设置初始值
        left_has_more, right_has_more, first, last = False, False, False, False
        page_number = page.number  # 获取当前页数
        total_pages = paginator.num_pages  # 获取总页数
        page_range = paginator.page_range  # 获得整个分页的页码表
        left = page_range[
            (page_number - 3) if (page_number - 3) > 0 else 0 : page_number - 1
        ]
        right = page_range[page_number : page_number + 2]
        if page_number == 1:
            left = []
            # 如果总页码-1比当前range最右边的页码还要大，说明右边连续页码不包括这一页 要加省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            # 如果最右边的页码比总页码要小所以需要显示最后一页的页码
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            # 如果当前页码减去3大于0 那么获取range（page-3，page-1）否则获取range（0，page-1）
            right = []
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            "left": left,
            "right": right,
            "left_has_more": left_has_more,
            "right_has_more": right_has_more,
            "first": first,
            "last": last,
        }
        return data


class ArchivesView(IndexView):
    model = Post
    template_name = "blog/archives/archives.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({"status": "archives"})
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(
            extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.codehilite",
                "markdown.extensions.toc",
                TocExtension(slugify=slugify),
            ]
        )
        post.body = md.convert(post.body)
        if len(md.toc) > 35:
            post.toc = md.toc
        return post


def category_list(request):
    return render(request, "blog/category/category.html")


class CategoryDetailView(IndexView):
    template_name = "blog/category/category_detail.html"
    paginate_by = 5

    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get("name"))
        return super(CategoryDetailView, self).get_queryset().filter(category=cate)


def post_tags(request):
    return render(request, "blog/tag/tags.html", {"status": "tags"})


class TagDetailView(IndexView):
    template_name = "blog/tag/tag_detail.html"

    def get_queryset(self):
        tags = get_object_or_404(Tag, name=self.kwargs.get("name"))
        return super(TagDetailView, self).get_queryset().filter(tags=tags)

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        tag = get_object_or_404(Tag, name=self.kwargs["name"])
        context.update({"tag": tag})
        return context
