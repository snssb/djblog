from django import template

from blog.models import Post, Tag

register = template.Library()


# @register.inclusion_tag('blog/popular_posts_tpl.html')
# def get_popular(cnt=3):
#     posts = Post.objects.raw('''SELECT *
#                                 FROM blog_post
#                                 LEFT JOIN blog_post_likes ON blog_post.id = blog_post_likes.post_id
#                                 GROUP BY blog_post.id ORDER BY COUNT(blog_post_likes.post_id) DESC'''
#                              )[:cnt]
#     return {"posts": posts}


@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.filter(is_published=True).order_by('-views')[:cnt]
    return {"posts": posts}


@register.inclusion_tag('blog/tags_tpl.html')
def get_tags():
    tags = Tag.objects.all()
    return {"tags": tags}

