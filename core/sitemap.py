from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    # Priority of the URL in the sitemap (from 0.0 to 1.0)
    priority = 0.8

    # Change frequency (e.g., 'daily', 'weekly', 'monthly')
    changefreq = 'weekly'

    def items(self):
        # Return all the items to be included in the sitemap
        return Post.objects.all()

    def lastmod(self, obj):
        # Return the last modification date for each object
        return obj.updated_at