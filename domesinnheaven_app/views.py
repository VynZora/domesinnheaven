from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Q
import requests
from urllib.parse import quote

from .forms import (
    BlogForm,
    ContactForm,
    TestimonialForm,
    ActivityForm,
    CampingPackageForm,
    BookingForm,
    DomeTypeForm,
)


from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from .models import Booking   # change this if Booking is imported from another app

from .models import (
    Blog,
    Category,
    ContactMessage,
    GalleryImage,
    Testimonial,
    Activity,
    CampingPackage,
    Booking,
    DomeType,
    DomeTypeImage,
    DomeFAQ
    

)


def home(request):
    testimonials = Testimonial.objects.all().order_by("-created_at")[:5]
    camping_packages = CampingPackage.objects.all().order_by("-created_at")[:6]
    activities = Activity.objects.all().order_by("-created_at")[:6]
    blogs = Blog.objects.all().order_by("-created_at")[:3]

    # Show every Dome Type
    dome_types = DomeType.objects.all().order_by("-created_at")

    return render(request, "frontend/index.html", {
        "testimonials": testimonials,
        "camping_packages": camping_packages,
        "activities": activities,
        "blogs": blogs,
        "dome_types": dome_types,
    })

# def home_v2(request):
#     """Luxury scrollytelling homepage — index_v2.html."""
#     testimonials = Testimonial.objects.all().order_by("-created_at")[:5]
#     camping_packages = CampingPackage.objects.all().order_by("-created_at")[:6]
#     activities = Activity.objects.all().order_by("-created_at")[:6]
#     blogs = Blog.objects.all().order_by("-created_at")[:3]
#     return render(request, 'frontend/index_v2.html', {
#         'testimonials': testimonials,
#         'camping_packages': camping_packages,
#         'activities': activities,
#         'blogs': blogs,
#         'clips_base_url': settings.CLOUDINARY_CLIPS_BASE_URL,
#     })

def about(request):
    testimonials = Testimonial.objects.all().order_by("-created_at")[:5]
    camping_packages = CampingPackage.objects.all().order_by("-created_at")[:6]
    dome_types = DomeType.objects.all().order_by("-created_at")

    return render(request, "frontend/about.html", {
        "testimonials": testimonials,
        "camping_packages": camping_packages,
        "dome_types": dome_types,
    })



def services(request):
    dome_types = DomeType.objects.all().order_by("-created_at")

    return render(request, "frontend/services.html", {
        "dome_types": dome_types,
    })



def services_details(request, slug):

    dome = get_object_or_404(
        DomeType.objects.prefetch_related(
            "images",
            "faqs",
        ),
        slug=slug,
    )

    recent_domes = (
        DomeType.objects
        .exclude(pk=dome.pk)
        .order_by("-created_at")[:5]
    )

    return render(
        request,
        "frontend/dome-unit-details.html",
        {
            "dome": dome,
            "recent_domes": recent_domes,
        }
    )




def activities(request):
    activities_qs = Activity.objects.all().order_by('-created_at')
    paginator = Paginator(activities_qs, 6) # Show 6 activities per page
    page_number = request.GET.get("page")
    activities_list = paginator.get_page(page_number)
    testimonials = Testimonial.objects.all().order_by("-created_at")[:5]
    return render(request, 'frontend/activities.html', {'activities': activities_list, 'testimonials': testimonials})

def activity_details(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    return render(request, 'frontend/activity-details.html', {'activity': activity})

def blog_grid(request):
    blogs_qs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs_qs, 9)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    testimonials = Testimonial.objects.all().order_by("-created_at")[:3]
    return render(request, "frontend/blog-grid.html", {"blogs": blogs, "testimonials": testimonials})

def blog_standard(request):
    return render(request, 'frontend/blog-standard.html')

def gallery(request):
    categories = Category.objects.all()
    gallery_images = GalleryImage.objects.select_related('category').all().order_by('-uploaded_at')
    return render(request, 'frontend/gallery.html', {
        'categories': categories,
        'gallery_images': gallery_images
    })

def blog_details(request, slug=None):
    if slug:
        blog = get_object_or_404(Blog, slug=slug)
    else:
        blog = Blog.objects.order_by("-created_at").first()
        if not blog:
            return redirect("blog_grid")
    recent_blogs = Blog.objects.exclude(id=blog.id).order_by("-created_at")[:4]
    testimonials = Testimonial.objects.all().order_by("-created_at")[:3]
    gallery_images = GalleryImage.objects.all().order_by('-uploaded_at')[:6]
    return render(
        request,
        "frontend/blog-details.html",
        {"blog": blog, "recent_blogs": recent_blogs, "testimonials": testimonials, "gallery_images": gallery_images},
    )

def camping(request):
    camping_packages = CampingPackage.objects.all().order_by("-created_at")

    return render(request, "frontend/camping.html", {
        "camping_packages": camping_packages,
    })


def camping_details(request, slug=None):
    if slug:
        package = get_object_or_404(CampingPackage, slug=slug)
    else:
        # Fallback for old URL if needed, or just redirect
        package = CampingPackage.objects.first()
    
    return render(request, 'frontend/camping-details.html', {'package': package})

def camping_donation(request):
    return render(request, 'frontend/camping-donation.html')

def donations(request):
    return render(request, 'frontend/donations.html')

def terms(request):
    return render(request, 'frontend/terms.html')

def contact(request):
    if request.method == "POST":
        # reCAPTCHA Validation
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            messages.error(request, "Please complete the reCAPTCHA.")
            return render(request, "frontend/contact.html", {"contact_form_data": request.POST})

        verify_data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=verify_data)
            result = r.json()
            if not result.get('success'):
                messages.error(request, "reCAPTCHA verification failed. Please try again.")
                return render(request, "frontend/contact.html", {"contact_form_data": request.POST})
        except Exception:
            # Fallback if request fails
            pass

        full_name = (request.POST.get("name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        email = (request.POST.get("email") or "").strip()
        user_message = (request.POST.get("message") or "").strip()

        location = (request.POST.get("location") or "").strip()
        contact_time = (request.POST.get("contact_time") or "").strip()

        if not full_name or not phone:
            messages.error(request, "Please enter your name and phone number.")
            return render(
                request,
                "frontend/contact.html",
                {"contact_form_data": request.POST},
            )

        name_parts = full_name.split(None, 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        final_message = user_message

        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email or None,
            message=final_message,
            best_time_to_contact=contact_time or None,
        )
        messages.success(request, "Your message has been sent successfully. We will contact you soon.")
        return redirect("contact")

    return render(request, 'frontend/contact.html')

def volunteer(request):
    return render(request, 'frontend/volunteer.html')

def volunteer_details(request):
    return render(request, 'frontend/volunteer-details.html')

def be_volunteer(request):
    return render(request, 'frontend/be-volunteer.html')

def page_not_found(request, exception):
    return render(request, 'frontend/404.html', status=404)


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, "authenticate/login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("admin_dashboard")

        messages.error(request, "Invalid credentials or unauthorized access.")

    return render(request, "authenticate/login.html")


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

@login_required(login_url="admin_login")
def admin_dashboard(request):
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 1. Total Stats
    stats = {
        'total_blogs': Blog.objects.count(),
        'blogs_this_month': Blog.objects.filter(created_at__gte=month_start).count(),
        'total_services': Category.objects.count(),
        'total_contacts': ContactMessage.objects.count(),
        'total_packages': CampingPackage.objects.count(),
        'total_activities': Activity.objects.count(),
        'total_dome_types': DomeType.objects.count(),
    }

    # 2. Recent Lists
    recent_blogs = Blog.objects.all().order_by('-created_at')[:4]
    recent_contacts = ContactMessage.objects.all().order_by('-created_at')[:4]
    recent_packages = CampingPackage.objects.all().order_by('-created_at')[:4]
    recent_activities = Activity.objects.all().order_by('-created_at')[:4]

    # 3. Chart Data (Blogs vs Contacts over last 6 months)
    month_labels = []
    blogs_counts = []
    contacts_counts = []
    
    for i in range(5, -1, -1):
        target_month = now - relativedelta(months=i)
        label = target_month.strftime('%b')
        month_labels.append(label)
        
        blogs_count = Blog.objects.filter(
            created_at__year=target_month.year,
            created_at__month=target_month.month
        ).count()
        blogs_counts.append(blogs_count)
        
        contacts_count = ContactMessage.objects.filter(
            created_at__year=target_month.year,
            created_at__month=target_month.month
        ).count()
        contacts_counts.append(contacts_count)
        
    # 4. Service Distribution (Doughnut Chart)
    service_labels = []
    service_counts = []
    for category in Category.objects.all()[:6]: # Limit to top 6 categories for visual fit
        service_labels.append(category.name)
        # Using GalleryImage count as a proxy for category size since there is no direct service linkage
        service_counts.append(category.images.count())
        
    if not service_labels: # Fallback if empty to load chart cleanly
        service_labels = ['No Data']
        service_counts = [1]

    context = {
        'stats': stats,
        'recent_blogs': recent_blogs,
        'recent_contacts': recent_contacts,
        'recent_packages': recent_packages,
        'recent_activities': recent_activities,
        'month_labels': month_labels,
        'blogs_counts': blogs_counts,
        'contacts_counts': contacts_counts,
        'service_labels': service_labels,
        'service_counts': service_counts,
    }

    return render(request, "admin_pages/dashboard.html", context)



# ==========================================
# 6. BLOGS (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def admin_blog_list(request):  # RENAMED from blog_list to fix URL error
    blogs_qs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs_qs, 6)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    return render(request, "admin_pages/blog_list.html", {"blogs": blogs})

@login_required(login_url="admin_login")
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post created!")
            return redirect("admin_blog_list")
    else:
        form = BlogForm()
    return render(request, "admin_pages/create_blog.html", {"form": form})

@login_required(login_url="admin_login")
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated!")
            return redirect("admin_blog_list")
    else:
        form = BlogForm(instance=blog)
    return render(request, "admin_pages/create_blog.html", {"form": form, "blog": blog})

@login_required(login_url="admin_login")
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted.")
    return redirect("admin_blog_list")


# ==========================================
# 7. GALLERY (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def gallery_images(request):
    categories = Category.objects.all().prefetch_related("images")
    category_pages = {}
    for category in categories:
        images_qs = category.images.all().order_by("-uploaded_at")
        paginator = Paginator(images_qs, 8)
        page_number = request.GET.get(f"page_{category.id}", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        category_pages[category.id] = page_obj

    return render(
        request, "admin_pages/image_list.html",
        {"categories": categories, "category_pages": category_pages},
    )

@login_required(login_url="admin_login")
def add_image(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist("images")
        for file in files:
            GalleryImage.objects.create(
                category=category,
                title=file.name,
                image=file,
            )
        messages.success(request, "Images uploaded successfully!")
        return redirect("list_image")

    return render(request, "admin_pages/add_image.html", {"categories": categories})

@login_required(login_url="admin_login")
def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image deleted successfully!")
        return redirect("list_image")
    return render(request, "admin_pages/image_list.html", {"image": image})


@login_required(login_url="admin_login")
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    return render(request, "admin_pages/category_list.html", {"categories": categories})


@login_required(login_url="admin_login")
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category created successfully!")
            return redirect("category_list")
    return render(request, "admin_pages/add_category.html")


@login_required(login_url="admin_login")
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect("category_list")
    return redirect("category_list")


@login_required(login_url="admin_login")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("category_list")
    return redirect("category_list")


# ==========================================
# 8. TESTIMONIALS (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def testimonial_list(request):
    testimonials_list = Testimonial.objects.all().order_by(Lower("name"))
    paginator = Paginator(testimonials_list, 6)
    page_number = request.GET.get("page")
    testimonials = paginator.get_page(page_number)
    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})


@login_required(login_url="admin_login")
def testimonial_create(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully!")
            return redirect("review_list")
    else:
        form = TestimonialForm()
    return render(request, "admin_pages/create_review.html", {"form": form})


@login_required(login_url="admin_login")
def testimonial_update(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully!")
            return redirect("review_list")
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, "admin_pages/review_list.html", {"form": form, "testimonial": testimonial})


@login_required(login_url="admin_login")
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully!")
        return redirect("review_list")
    return render(request, "admin_pages/review_list.html", {"testimonial": testimonial})


# ==========================================
# 9. CONTACTS & INQUIRIES (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def view_contacts(request):
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    contacts = ContactMessage.objects.all().order_by("-created_at")
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "admin_pages/view_contacts.html", {"contacts": page_obj})

@login_required(login_url="admin_login")
def delete_contact(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        contact.delete()
    return redirect("view_contacts")


# ==========================================
# 9.5 BOOKINGS (FRONTEND AND ADMIN)
# ==========================================


from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import BookingForm


# ============================================================
# BOOKING - FRONTEND
# ============================================================

def booking(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            # Save booking.
            #
            # BookingForm now contains:
            # name
            # phone
            # email
            # guests
            # check_in
            # check_out
            # dome_type
            # message
            #
            # No Add-ons
            # No Jacuzzi Bathtub

            booking_obj = form.save()

            messages.success(
                request,
                "Booking request sent successfully. "
                "We will contact you soon."
            )

            return redirect("booking")

        # Form validation failed
        messages.error(
            request,
            "Please check the form and correct "
            "the errors below."
        )

    else:

        form = BookingForm()

    return render(
        request,
        "frontend/booking.html",
        {
            "form": form,
        }
    )



# @login_required(login_url="admin_login")
# def admin_view_bookings(request):
#     Booking.objects.filter(is_read=False).update(is_read=True)
#     bookings = Booking.objects.all().order_by("-created_at")
#     paginator = Paginator(bookings, 10)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     return render(request, "admin_pages/view_bookings.html", {"bookings": page_obj})



# ============================================================
# BOOKINGS - ADMIN LIST
# ============================================================

@login_required(login_url="admin_login")
def admin_view_bookings(request):

    # ========================================================
    # MARK UNREAD BOOKINGS AS READ
    # ========================================================

    Booking.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )


    # ========================================================
    # BASE QUERYSET
    # ========================================================

    bookings_qs = (
        Booking.objects
        .select_related(
            "dome_type",
            "camping_package",
        )
        .order_by("-created_at")
    )


    # ========================================================
    # SEARCH
    # ========================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        bookings_qs = bookings_qs.filter(

            Q(name__icontains=search)

            | Q(phone__icontains=search)

            | Q(email__icontains=search)

            | Q(message__icontains=search)

            | Q(
                dome_type__name__icontains=search
            )

            | Q(
                camping_package__name__icontains=search
            )
        )


    # ========================================================
    # DATE FROM
    # ========================================================

    date_from = request.GET.get(
        "date_from",
        ""
    ).strip()

    if date_from:

        bookings_qs = bookings_qs.filter(
            created_at__date__gte=date_from
        )


    # ========================================================
    # DATE TO
    # ========================================================

    date_to = request.GET.get(
        "date_to",
        ""
    ).strip()

    if date_to:

        bookings_qs = bookings_qs.filter(
            created_at__date__lte=date_to
        )


    # ========================================================
    # PAGINATION
    # ========================================================

    paginator = Paginator(
        bookings_qs,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )


    # ========================================================
    # CONTEXT
    # ========================================================

    context = {
        "bookings": page_obj,
        "search": search,
        "date_from": date_from,
        "date_to": date_to,
    }


    # ========================================================
    # PAGE
    # ========================================================

    return render(
        request,
        "admin_pages/view_bookings.html",
        context
    )



@login_required(login_url="admin_login")
def admin_delete_booking(request, pk):
    booking_obj = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        booking_obj.delete()
        messages.success(request, "Booking deleted successfully!")
    return redirect("admin_view_bookings")


# ==========================================
# 10. ACTIVITIES (FRONTEND)
# ==========================================

def activity_list(request):
    # Fetch activities, ordered by newest first
    activities_qs = Activity.objects.all().order_by("-created_at")
    paginator = Paginator(activities_qs, 9)
    page_number = request.GET.get("page")
    activities = paginator.get_page(page_number)
    testimonials = list(Testimonial.objects.all()[:8])
    if testimonials and len(testimonials) < 3:
        repeat_count = (3 + len(testimonials) - 1) // len(testimonials)
        testimonials = (testimonials * repeat_count)[:3]
    return render(request, "frontend/activities.html", {"activities": activities, "testimonials": testimonials})


def activity_single(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    # Optional: fetch other recent activities for a sidebar
    recent_activities = Activity.objects.exclude(slug=slug)[:3]
    context = {"activity": activity, "recent_activities": recent_activities}
    return render(request, "frontend/activity-single.html", context)


# ==========================================
# 11. ACTIVITIES (ADMIN DASHBOARD)
# ==========================================

@login_required(login_url="admin_login")
def admin_activity_list(request):
    activities_qs = Activity.objects.all().order_by("-created_at")
    paginator = Paginator(activities_qs, 10)
    page_number = request.GET.get("page")
    activities = paginator.get_page(page_number)
    return render(request, "admin_pages/activity_list.html", {"activities": activities})


@login_required(login_url="admin_login")
def activity_create(request):
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity created successfully!")
            return redirect("admin_activity_list")
    else:
        form = ActivityForm()
    return render(request, "admin_pages/create_activity.html", {"form": form})


@login_required(login_url="admin_login")
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            return redirect("admin_activity_list")
    else:
        form = ActivityForm(instance=activity)
    # Reusing the create template for editing is common practice
    return render(request, "admin_pages/create_activity.html", {"form": form, "activity": activity})


@login_required(login_url="admin_login")
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.delete()
        messages.success(request, "Activity deleted successfully!")
    return redirect("admin_activity_list")


# ==========================================
# 12. CAMPING PACKAGES (FRONTEND)
# ==========================================




# def service_single(request, slug):
#     category = get_object_or_404(DomeCategory, slug=slug)
#     domes_qs = category.domes.all().order_by("-created_at")
    
#     paginator = Paginator(domes_qs, 9)
#     page_number = request.GET.get("page")
#     domes = paginator.get_page(page_number)
    
#     recent_categories = DomeCategory.objects.exclude(slug=slug).order_by("name")[:5]
#     return render(request, "frontend/dome-category-details.html", {
#         "category": category, 
#         "domes": domes,
#         "recent_categories": recent_categories
#     })


# ==========================================
# 13. CAMPING PACKAGES (ADMIN DASHBOARD)
# ==========================================

@login_required(login_url="admin_login")
def admin_camping_package_list(request):
    packages_qs = CampingPackage.objects.all().order_by("-created_at")
    paginator = Paginator(packages_qs, 10)
    page_number = request.GET.get("page")
    packages = paginator.get_page(page_number)
    return render(request, "admin_pages/camping_package_list.html", {"packages": packages})


@login_required(login_url="admin_login")
def camping_package_create(request):
    if request.method == "POST":
        form = CampingPackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Camping Package created successfully!")
            return redirect("admin_camping_package_list")
    else:
        form = CampingPackageForm()
    return render(request, "admin_pages/create_camping_package.html", {"form": form})


@login_required(login_url="admin_login")
def camping_package_update(request, pk):
    package = get_object_or_404(CampingPackage, pk=pk)
    if request.method == "POST":
        form = CampingPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Camping Package updated successfully!")
            return redirect("admin_camping_package_list")
    else:
        form = CampingPackageForm(instance=package)
    return render(request, "admin_pages/create_camping_package.html", {"form": form, "package": package})


@login_required(login_url="admin_login")
def camping_package_delete(request, pk):
    package = get_object_or_404(CampingPackage, pk=pk)
    if request.method == "POST":
        package.delete()
        messages.success(request, "Camping Package deleted successfully!")
    return redirect("admin_camping_package_list")

# ==========================================
# 15. DOME CATEGORIES (ADMIN DASHBOARD)
# ==========================================

# @login_required(login_url="admin_login")
# def admin_dome_category_list(request):
#     categories_qs = DomeCategory.objects.all().order_by("-created_at")
#     paginator = Paginator(categories_qs, 10)
#     page_number = request.GET.get("page")
#     categories = paginator.get_page(page_number)
#     return render(request, "admin_pages/dome_category_list.html", {"categories": categories})

# @login_required(login_url="admin_login")
# def dome_category_create(request):
#     if request.method == "POST":
#         form = DomeCategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Dome category created successfully!")
#             return redirect("admin_dome_category_list")
#     else:
#         form = DomeCategoryForm()
#     return render(request, "admin_pages/create_dome_category.html", {"form": form})

# @login_required(login_url="admin_login")
# def dome_category_update(request, pk):
#     category = get_object_or_404(DomeCategory, pk=pk)
#     if request.method == "POST":
#         form = DomeCategoryForm(request.POST, request.FILES, instance=category)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Dome category updated successfully!")
#             return redirect("admin_dome_category_list")
#     else:
#         form = DomeCategoryForm(instance=category)
#     return render(request, "admin_pages/create_dome_category.html", {"form": form, "category": category})

# @login_required(login_url="admin_login")
# def dome_category_delete(request, pk):
#     category = get_object_or_404(DomeCategory, pk=pk)
#     if request.method == "POST":
#         category.delete()
#         messages.success(request, "Dome category deleted successfully!")
#     return redirect("admin_dome_category_list")

# ==========================================
# 16. DOME TYPES (ADMIN DASHBOARD)
# ==========================================

# ==========================================
# DOME TYPES (ADMIN DASHBOARD)
# ==========================================

@login_required(login_url="admin_login")
def admin_dome_type_list(request):

    dome_types_qs = (
        DomeType.objects
        .prefetch_related(
            "images",
            "faqs",
        )
        .order_by("-created_at")
    )


    paginator = Paginator(
        dome_types_qs,
        10,
    )


    page_number = request.GET.get(
        "page"
    )


    dome_types = paginator.get_page(
        page_number
    )


    return render(
        request,
        "admin_pages/dome_type_list.html",
        {
            "dome_types": dome_types,
        }
    )



# @login_required(login_url="admin_login")
# def dome_type_create(request):
#     if request.method == "POST":
#         form = DomeTypeForm(request.POST, request.FILES)

#         if form.is_valid():
#             dome_type = form.save()

#             messages.success(
#                 request,
#                 f'"{dome_type.name}" created successfully!'
#             )

#             return redirect("admin_dome_type_list")

#         print("DOME TYPE CREATE ERRORS:")
#         print(form.errors)
#         print(form.errors.as_data())

#         messages.error(
#             request,
#             "Dome type could not be created. Please correct the errors below."
#         )

#     else:
#         form = DomeTypeForm()

#     return render(
#         request,
#         "admin_pages/create_dome_type.html",
#         {
#             "form": form,
#             "dome_type": None,
#         }
#     )



@login_required(login_url="admin_login")
def dome_type_create(request):

    if request.method == "POST":

        form = DomeTypeForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            # =====================================================
            # GET UPLOADED DOME IMAGES
            # =====================================================

            images = request.FILES.getlist("images")


            # =====================================================
            # REQUIRE AT LEAST ONE IMAGE
            # =====================================================

            if not images:

                form.add_error(
                    "images",
                    "Please select at least one dome image.",
                )

            else:

                # =================================================
                # CREATE DOME
                # =================================================

                dome_type = form.save(commit=False)

                # main_image will point to the first
                # DomeTypeImage after upload.
                dome_type.main_image = None

                dome_type.save()


                # =================================================
                # SAVE DOME GALLERY IMAGES
                # =================================================

                first_gallery_image = None

                for uploaded_image in images:

                    gallery_image = (
                        DomeTypeImage.objects.create(
                            dome_type=dome_type,
                            image=uploaded_image,
                        )
                    )

                    if first_gallery_image is None:
                        first_gallery_image = gallery_image


                # =================================================
                # SET FIRST GALLERY IMAGE AS MAIN IMAGE
                # =================================================

                if first_gallery_image:

                    DomeType.objects.filter(
                        pk=dome_type.pk
                    ).update(
                        main_image=first_gallery_image.image.name
                    )


                # =================================================
                # SAVE FAQS
                # =================================================

                faq_questions = request.POST.getlist(
                    "faq_question[]"
                )

                faq_answers = request.POST.getlist(
                    "faq_answer[]"
                )


                for index, question in enumerate(
                    faq_questions
                ):

                    question = question.strip()

                    answer = ""

                    if index < len(faq_answers):
                        answer = faq_answers[index].strip()


                    # ---------------------------------------------
                    # Ignore empty FAQ row
                    # ---------------------------------------------

                    if not question and not answer:
                        continue


                    # ---------------------------------------------
                    # Save only when both question + answer exist
                    # ---------------------------------------------

                    if question and answer:

                        DomeFAQ.objects.create(
                            dome_type=dome_type,
                            question=question,
                            answer=answer,
                            order=index,
                            is_active=True,
                        )


                # =================================================
                # SUCCESS
                # =================================================

                messages.success(
                    request,
                    f'"{dome_type.name}" created successfully!',
                )

                return redirect(
                    "admin_dome_type_list"
                )


        # =========================================================
        # FORM ERROR
        # =========================================================

        messages.error(
            request,
            "Dome type could not be created. "
            "Please correct the errors below.",
        )


    else:

        form = DomeTypeForm()


    # =============================================================
    # PAGE
    # =============================================================

    return render(
        request,
        "admin_pages/create_dome_type.html",
        {
            "form": form,
            "dome_type": None,
        },
    )




@login_required(login_url="admin_login")
def dome_type_update(request, pk):

    # =============================================================
    # GET DOME
    # =============================================================

    dome = get_object_or_404(
        DomeType.objects.prefetch_related(
            "images",
            "faqs",
        ),
        pk=pk,
    )


    # =============================================================
    # ONLY POST IS USED FOR UPDATE
    # =============================================================

    if request.method != "POST":

        return redirect(
            "admin_dome_type_list"
        )


    # =============================================================
    # IMPORTANT
    #
    # Do NOT give request.FILES to DomeTypeForm.
    #
    # Gallery images are manually handled below.
    # =============================================================

    form = DomeTypeForm(
        request.POST,
        instance=dome,
    )


    # =============================================================
    # VALIDATE FORM
    # =============================================================

    if not form.is_valid():

        print("DOME UPDATE ERRORS:")
        print(form.errors)
        print(form.errors.as_data())

        messages.error(
            request,
            "Please correct the errors and try again.",
        )

        return redirect(
            "admin_dome_type_list"
        )


    # =============================================================
    # GET NEW IMAGES
    # =============================================================

    new_images = request.FILES.getlist(
        "images"
    )


    # =============================================================
    # GET EXISTING IMAGES SELECTED FOR DELETION
    # =============================================================

    delete_image_ids = request.POST.getlist(
        "delete_images"
    )


    # =============================================================
    # UPDATE NORMAL DOME FIELDS
    # =============================================================

    dome = form.save(commit=False)

    # Keep current main image.
    # Do not assign uploaded temporary files here.

    dome.save()


    # =============================================================
# UPDATE MULTIPLE FAQS
# =============================================================

    faq_questions = request.POST.getlist("faq_question[]")
    faq_answers = request.POST.getlist("faq_answer[]")

# Make sure each question has a matching answer
    if len(faq_questions) != len(faq_answers):
        messages.error(
        request,
        "FAQ data is incomplete. Please try again."
       )
        return redirect("admin_dome_type_list")

    faq_data = []

    for question, answer in zip(faq_questions, faq_answers):
        question = question.strip()
        answer = answer.strip()

    # Ignore completely empty FAQ rows
        if not question and not answer:
            continue

    # Do not silently discard incomplete FAQs
        if not question or not answer:
           messages.error(
            request,
            "Every FAQ must have both a question and an answer."
          )
           return redirect("admin_dome_type_list")

        if len(question) > 255:
            messages.error(
            request,
            "FAQ questions cannot exceed 255 characters."
           )
            return redirect("admin_dome_type_list")

        faq_data.append((question, answer))


# Save FAQs together in a database transaction
    from django.db import transaction

    with transaction.atomic():

    # Delete old FAQ records only after validating the new list
        DomeFAQ.objects.filter(dome_type=dome).delete()

    # Save all submitted FAQs
        for index, (question, answer) in enumerate(faq_data):

           DomeFAQ.objects.create(
              dome_type=dome,
               question=question,
              answer=answer,
              order=index,
              is_active=True,
        )


    # =============================================================
    # CURRENT MAIN IMAGE
    # =============================================================

    current_main_name = (
        dome.main_image.name
        if dome.main_image
        else None
    )

    main_was_deleted = False


    # =============================================================
    # DELETE SELECTED EXISTING GALLERY IMAGES
    # =============================================================

    if delete_image_ids:

        images_to_delete = list(
            DomeTypeImage.objects.filter(
                dome_type=dome,
                pk__in=delete_image_ids,
            )
        )


        for gallery_image in images_to_delete:

            if (
                current_main_name
                and
                gallery_image.image.name
                == current_main_name
            ):

                main_was_deleted = True


            gallery_image.delete()


    # =============================================================
    # SAVE NEW IMAGES
    # =============================================================

    first_new_gallery_image = None


    for uploaded_image in new_images:

        gallery_image = (
            DomeTypeImage.objects.create(
                dome_type=dome,
                image=uploaded_image,
            )
        )


        if first_new_gallery_image is None:

            first_new_gallery_image = gallery_image


    # =============================================================
    # DETERMINE NEW MAIN IMAGE
    # =============================================================

    new_main_image_name = None


    # -------------------------------------------------------------
    # If new images are uploaded,
    # first new image becomes main image
    # -------------------------------------------------------------

    if first_new_gallery_image:

        new_main_image_name = (
            first_new_gallery_image.image.name
        )


    # -------------------------------------------------------------
    # If current main image was deleted and no new image exists,
    # use first remaining gallery image
    # -------------------------------------------------------------

    elif main_was_deleted:

        remaining_image = (
            DomeTypeImage.objects
            .filter(dome_type=dome)
            .order_by("id")
            .first()
        )


        if remaining_image:

            new_main_image_name = (
                remaining_image.image.name
            )


    # =============================================================
    # UPDATE MAIN IMAGE
    # =============================================================

    if new_main_image_name:

        DomeType.objects.filter(
            pk=dome.pk
        ).update(
            main_image=new_main_image_name
        )


    elif main_was_deleted:

        DomeType.objects.filter(
            pk=dome.pk
        ).update(
            main_image=None
        )


    # =============================================================
    # SUCCESS
    # =============================================================

    messages.success(
        request,
        f'"{dome.name}" updated successfully.',
    )


    return redirect(
        "admin_dome_type_list"
    )




@login_required(login_url="admin_login")
def dome_type_delete(request, pk):
    dome_type = get_object_or_404(
        DomeType,
        pk=pk
    )

    if request.method == "POST":
        dome_name = dome_type.name

        dome_type.delete()

        messages.success(
            request,
            f'"{dome_name}" deleted successfully!'
        )

    return redirect("admin_dome_type_list")




# ============================================================
# DOWNLOAD BOOKINGS AS EXCEL
# ============================================================

@login_required(login_url="admin_login")
def admin_download_bookings_excel(request):

    # ========================================================
    # BASE QUERYSET
    # ========================================================

    bookings = (
        Booking.objects
        .select_related(
            "dome_type",
            "camping_package",
        )
        .order_by("-created_at")
    )


    # ========================================================
    # EXPORT TYPE
    #
    # all      = all bookings
    # page     = current page
    # filtered = all filtered bookings
    # ========================================================

    export_type = request.GET.get(
        "type",
        "all"
    )


    # ========================================================
    # SEARCH FILTER
    # ========================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        bookings = bookings.filter(

            Q(name__icontains=search)

            | Q(phone__icontains=search)

            | Q(email__icontains=search)

            | Q(message__icontains=search)

            | Q(
                dome_type__name__icontains=search
            )

            | Q(
                camping_package__name__icontains=search
            )
        )


    # ========================================================
    # DATE FILTER
    # ========================================================

    date_from = request.GET.get(
        "date_from",
        ""
    ).strip()

    date_to = request.GET.get(
        "date_to",
        ""
    ).strip()


    if date_from:

        bookings = bookings.filter(
            created_at__date__gte=date_from
        )


    if date_to:

        bookings = bookings.filter(
            created_at__date__lte=date_to
        )


    # ========================================================
    # CURRENT PAGE EXPORT
    # ========================================================

    page_number = request.GET.get(
        "page",
        1
    )

    if export_type == "page":

        paginator = Paginator(
            bookings,
            10
        )

        page_obj = paginator.get_page(
            page_number
        )

        bookings = page_obj.object_list


    # ========================================================
    # CREATE EXCEL WORKBOOK
    # ========================================================

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Bookings"


    # ========================================================
    # HEADERS
    # ========================================================

    headers = [
        "Booking ID",
        "Date Posted",
        "Name",
        "Phone",
        "Email",
        "Check In",
        "Check Out",
        "Guests",
        "Dome Type",
        "Camping Package",
        "Message",
        "Status",
    ]

    worksheet.append(headers)


    # ========================================================
    # HEADER STYLE
    # ========================================================

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="1F4E78"
    )

    header_font = Font(
        color="FFFFFF",
        bold=True
    )

    thin_border = Border(

        left=Side(
            style="thin",
            color="D9E2F3"
        ),

        right=Side(
            style="thin",
            color="D9E2F3"
        ),

        top=Side(
            style="thin",
            color="D9E2F3"
        ),

        bottom=Side(
            style="thin",
            color="D9E2F3"
        ),
    )


    for cell in worksheet[1]:

        cell.fill = header_fill

        cell.font = header_font

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        cell.border = thin_border


    # ========================================================
    # BOOKING DATA
    # ========================================================

    for booking_obj in bookings:


        # ----------------------------------------------------
        # DOME TYPE
        # ----------------------------------------------------

        if booking_obj.dome_type:

            dome_type_name = (
                booking_obj.dome_type.name
            )

        else:

            dome_type_name = "Not Selected"


        # ----------------------------------------------------
        # CAMPING PACKAGE
        # ----------------------------------------------------

        if booking_obj.camping_package:

            camping_package_name = (
                booking_obj.camping_package.name
            )

        else:

            camping_package_name = "Not Selected"


        # ----------------------------------------------------
        # READ STATUS
        # ----------------------------------------------------

        if booking_obj.is_read:

            read_status = "Read"

        else:

            read_status = "Unread"


        # ----------------------------------------------------
        # ADD EXCEL ROW
        # ----------------------------------------------------

        worksheet.append([

            booking_obj.id,

            (
                booking_obj.created_at.strftime(
                    "%d-%m-%Y %I:%M %p"
                )
                if booking_obj.created_at
                else ""
            ),

            booking_obj.name or "",

            booking_obj.phone or "",

            booking_obj.email or "",

            (
                booking_obj.check_in.strftime(
                    "%d-%m-%Y"
                )
                if booking_obj.check_in
                else ""
            ),

            (
                booking_obj.check_out.strftime(
                    "%d-%m-%Y"
                )
                if booking_obj.check_out
                else ""
            ),

            booking_obj.guests or 0,

            dome_type_name,

            camping_package_name,

            booking_obj.message or "",

            read_status,
        ])


    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    column_widths = {
        "A": 12,
        "B": 23,
        "C": 22,
        "D": 18,
        "E": 32,
        "F": 15,
        "G": 15,
        "H": 10,
        "I": 28,
        "J": 30,
        "K": 45,
        "L": 15,
    }


    for column, width in column_widths.items():

        worksheet.column_dimensions[
            column
        ].width = width


    # ========================================================
    # BODY STYLE
    # ========================================================

    for row in worksheet.iter_rows(
        min_row=2,
        max_row=worksheet.max_row
    ):

        for cell in row:

            cell.alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

            cell.border = thin_border


    # ========================================================
    # FREEZE HEADER + FILTER
    # ========================================================

    worksheet.freeze_panes = "A2"

    worksheet.auto_filter.ref = (
        f"A1:L{worksheet.max_row}"
    )


    # ========================================================
    # FILE NAME
    # ========================================================

    if export_type == "page":

        filename = (
            f"bookings_page_{page_number}.xlsx"
        )

    elif export_type == "filtered":

        filename = "filtered_bookings.xlsx"

    else:

        filename = "all_bookings.xlsx"


    # ========================================================
    # HTTP RESPONSE
    # ========================================================

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        )
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; filename="{filename}"'
    )

    workbook.save(response)

    return response