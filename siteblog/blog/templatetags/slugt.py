# from django import template
from django.template.defaultfilters import slugify

from blog.models import Post

#
# register = template.Library()



alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def dj_slug(s):
    """slugify для ru"""

    s = '-'.join(s.split())
    k = slugify(''.join(alphabet.get(w, w) for w in s.lower()))
    chk = Post.objects.filter(slug__contains=k).order_by('created_at')
    if chk:
        chk = chk.last().slug
        if not chk[-1].isdigit():
            k += '_1'
        else:
            k = chk[:chk.rfind('_')+1] + str(int(chk[chk.rfind('_')+1:]) + 1)

    return k
