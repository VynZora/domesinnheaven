"""
URL configuration for domesinnheaven_pro project.
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
    DomeTypeSitemap,
    StaticViewSitemap,
)


# ============================================================
# ERROR HANDLERS
# ============================================================

handler404 = "domesinnheaven_app.views.page_not_found"


# ============================================================
# SITEMAPS
# ============================================================

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
    "camping_package": CampingPackageSitemap,
    "activity": ActivitySitemap,
    "dome_type": DomeTypeSitemap,
}


# ============================================================
# ROBOTS.TXT
# ============================================================

def robots_txt(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        "domesinnheaven_pro",
        "robots.txt"
    )

    with open(file_path, "r") as file:
        return HttpResponse(
            file.read(),
            content_type="text/plain"
        )


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # Main application
    path(
        "",
        include("domesinnheaven_app.urls")
    ),

    # Robots
    path(
        "robots.txt",
        robots_txt,
        name="robots_txt"
    ),

    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap"
    ),
]


# ============================================================
# MEDIA FILES - DEVELOPMENT
# ============================================================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)