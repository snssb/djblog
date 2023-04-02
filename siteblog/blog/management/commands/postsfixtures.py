from django.core.management import call_command
from django.core.management.base import BaseCommand
from blog.models import Post


class Command(BaseCommand):
    help = 'My custom command for loading fixtures and logging posts'

    def handle(self, *args, **options):
        call_command('loaddata', 'blog/fixtures/posts.json')
        self.stdout.write(self.style.SUCCESS('Fixtures loaded successfully!'))

        for post in Post.objects.all():
            post.save()
            # self.stdout.write(self.style.SUCCESS(f'Post "{post.title}" has been logged successfully!'))