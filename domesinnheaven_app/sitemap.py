from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog, Activity, CampingPackage, DomeCategory, DomeType


class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return [
            "home",
            "about",
            "services",
            "activities",
            "gallery",
            "blog_grid",
            "camping",
            "contact",
            "booking",
            "terms",
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return reverse("blog_detail_slug", kwargs={"slug": obj.slug})


class CampingPackageSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return CampingPackage.objects.all()

    def location(self, obj):
        return reverse("package_details", kwargs={"slug": obj.slug})


class ActivitySitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Activity.objects.all()

    def location(self, obj):
        return reverse("activity_details", kwargs={"slug": obj.slug})


class DomeCategorySitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return DomeCategory.objects.all()

    def location(self, obj):
        return reverse("service_single", kwargs={"slug": obj.slug})


class DomeTypeSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return DomeType.objects.all()

    def location(self, obj):
        return reverse("services_details_with_slug", kwargs={"slug": obj.slug})
