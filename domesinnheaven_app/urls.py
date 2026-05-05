from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('preview/', views.home_v2, name='home_v2'),

    path('about/', views.about, name='about'),

    path('dome/', views.services, name='services'),
    path('dome/<slug:slug>/', views.service_single, name='service_single'),
    path('dome-details/', views.services_details, name='services_details'),
    path('dome-details/<slug:slug>/', views.services_details, name='services_details_with_slug'),
    path('ajax/load-dome-types/', views.load_dome_types, name='ajax_load_dome_types'),

    path('activities/', views.activities, name='activities'),
    path('activities/<slug:slug>/', views.activity_details, name='activity_details'),
    
    path('gallery/', views.gallery, name='gallery'),

    path('blogs/', views.blog_grid, name='blog_grid'),
    path('blog-standard/', views.blog_standard, name='blog_standard'),
    path('blog-details/', views.blog_details, name='blog_details'),
    path('blogs/<slug:slug>/', views.blog_details, name='blog_detail_slug'),

    path('camping/', views.camping, name='camping'),
    path('camping-details/', views.camping_details, name='camping_details'),
    path('camping/<slug:slug>/', views.camping_details, name='package_details'),
    path('camping-donation/', views.camping_donation, name='camping_donation'),

    path('donations/', views.donations, name='donations'),

    path('contact/', views.contact, name='contact'),

    path('volunteer/', views.volunteer, name='volunteer'),
    path('volunteer-details/', views.volunteer_details, name='volunteer_details'),
    path('be-volunteer/', views.be_volunteer, name='be_volunteer'),

    
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("dashboard/blogs/", views.admin_blog_list, name="admin_blog_list"),
    path("dashboard/blogs/create/", views.blog_create, name="blog_create"),
    path("dashboard/blogs/<int:pk>/edit/", views.blog_update, name="blog_update"),
    path("dashboard/blogs/<int:pk>/delete/", views.blog_delete, name="blog_delete"),

    path("dashboard/gallery/", views.gallery_images, name="list_image"),
    path("dashboard/gallery/add/", views.add_image, name="add_image"),
    path("dashboard/gallery/<int:image_id>/delete/", views.delete_image, name="delete_image"),

    path("dashboard/categories/", views.category_list, name="category_list"),
    path("dashboard/categories/add/", views.add_category, name="add_category"),
    path("dashboard/categories/<int:pk>/edit/", views.update_category, name="update_category"),
    path("dashboard/categories/<int:pk>/delete/", views.delete_category, name="delete_category"),

    path("dashboard/testimonials/", views.testimonial_list, name="review_list"),
    path("dashboard/testimonials/add/", views.testimonial_create, name="testimonial_create"),
    path("dashboard/testimonials/<int:pk>/edit/", views.testimonial_update, name="testimonial_update"),
    path("dashboard/testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),

    path("dashboard/activities/", views.admin_activity_list, name="admin_activity_list"),
    path("dashboard/activities/create/", views.activity_create, name="activity_create"),
    path("dashboard/activities/<int:pk>/edit/", views.activity_update, name="activity_update"),
    path("dashboard/activities/<int:pk>/delete/", views.activity_delete, name="activity_delete"),

    path("dashboard/camping-packages/", views.admin_camping_package_list, name="admin_camping_package_list"),
    path("dashboard/camping-packages/create/", views.camping_package_create, name="camping_package_create"),
    path("dashboard/camping-packages/<int:pk>/edit/", views.camping_package_update, name="camping_package_update"),
    path("dashboard/camping-packages/<int:pk>/delete/", views.camping_package_delete, name="camping_package_delete"),

    path("dashboard/contacts/", views.view_contacts, name="view_contacts"),
    path("dashboard/contacts/<int:pk>/delete/", views.delete_contact, name="delete_contact"),

    path("booking/", views.booking, name="booking"),
    path("dashboard/bookings/", views.admin_view_bookings, name="admin_view_bookings"),
    path("dashboard/bookings/<int:pk>/delete/", views.admin_delete_booking, name="admin_delete_booking"),

    path("dashboard/dome-categories/", views.admin_dome_category_list, name="admin_dome_category_list"),
    path("dashboard/dome-categories/add/", views.dome_category_create, name="dome_category_create"),
    path("dashboard/dome-categories/<int:pk>/edit/", views.dome_category_update, name="dome_category_update"),
    path("dashboard/dome-categories/<int:pk>/delete/", views.dome_category_delete, name="dome_category_delete"),

    path("dashboard/dome-types/", views.admin_dome_type_list, name="admin_dome_type_list"),
    path("dashboard/dome-types/add/", views.dome_type_create, name="dome_type_create"),
    path("dashboard/dome-types/<int:pk>/edit/", views.dome_type_update, name="dome_type_update"),
    path("dashboard/dome-types/<int:pk>/delete/", views.dome_type_delete, name="dome_type_delete"),
]
