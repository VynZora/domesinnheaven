"""
URL configuration for domesinnheaven_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from domesinnheaven_app.sitemap import (
    ActivitySitemap,
    BlogSitemap,
    CampingPackageSitemap,
    DomeCategorySitemap,
    DomeTypeSitemap,
    StaticViewSitemap,
)

handler404 = "domesinnheaven_app.views.page_not_found"

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
    "camping_package": CampingPackageSitemap,
    "activity": ActivitySitemap,
    "dome_category": DomeCategorySitemap,
    "dome_type": DomeTypeSitemap,
}


def robots_txt(request):
    file_path = os.path.join(settings.BASE_DIR, "domesinnheaven_pro", "robots.txt")
    with open(file_path, "r") as file:
        return HttpResponse(file.read(), content_type="text/plain")

urlpatterns = [
    path('', include('domesinnheaven_app.urls')),
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
