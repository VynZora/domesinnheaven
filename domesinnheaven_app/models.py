from django.db import models
from django.utils.text import slugify
from .utils.image_optimizer import optimize_image

# class TeamMember(models.Model):
#     name = models.CharField(max_length=100)  
#     position = models.CharField(max_length=100)
#     photo = models.ImageField(upload_to='team/', blank=True, null=True)
#     bio = models.TextField(blank=True, help_text="Short introduction or quote.")
    
#     def __str__(self):
#         return f"{self.name} - {self.position}"

class OptimizedImageModel(models.Model):
    image_fields = []

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for field in self.image_fields:
            image_field = getattr(self, field, None)
            if image_field and hasattr(image_field, "path"):
                optimize_image(image_field.path)


class DomeCategory(OptimizedImageModel):
    image_fields = ["image"]
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="dome_categories/", help_text="Category cover image")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dome Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class DomeType(OptimizedImageModel):
    image_fields = ["main_image"]
    category = models.ForeignKey(DomeCategory, on_delete=models.CASCADE, related_name="domes")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    main_image = models.ImageField(upload_to="domes/")
    
    check_in = models.CharField(max_length=20, default="12:00 PM")
    check_out = models.CharField(max_length=20, default="11:00 AM")
    
    normal_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    special_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    package_items = models.TextField(help_text="Enter items separated by new lines")
    facilities = models.TextField(help_text="Enter facilities separated by new lines")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dome Type"
        verbose_name_plural = "Dome Types"

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_package_items_list(self):
        return [item.strip() for item in self.package_items.split('\n') if item.strip()]

    def get_facilities_list(self):
        return [item.strip() for item in self.facilities.split('\n') if item.strip()]

class CampingPackage(OptimizedImageModel):
    image_fields = ["main_image"]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    main_image = models.ImageField(upload_to="camping/")
    
    check_in = models.CharField(max_length=20)
    check_out = models.CharField(max_length=20)
    
    normal_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    special_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    package_items = models.TextField()
    facilities = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Camping Packages"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class GalleryImage(OptimizedImageModel):
    image_fields = ["image"]

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="images"
    )
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"


class Activity(OptimizedImageModel):
    image_fields = ["image"]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="activities/", help_text="Activity cover image")
    duration = models.CharField(max_length=100, blank=True, help_text="Duration (e.g., 3 Days, 2 Hours)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Activity.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Blog(OptimizedImageModel):
    image_fields = ["image"]

    image = models.ImageField(upload_to="blogs/", help_text="Blog cover image")
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
class Testimonial(OptimizedImageModel):
    image_fields = ["image"]

    name = models.CharField(
        max_length=100, help_text="Name of the person giving the testimonial"
    )
    image = models.ImageField(
        upload_to="testimonials/", blank=True, null=True, help_text="Profile picture"
    )
    review = models.TextField(help_text="Customer or client review")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True) 
    message = models.TextField(blank=True)
    best_time_to_contact = models.CharField(max_length=100, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    camping_package = models.ForeignKey(CampingPackage, on_delete=models.SET_NULL, null=True, blank=True)
    dome_category = models.ForeignKey(DomeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    dome_type = models.ForeignKey(DomeType, on_delete=models.SET_NULL, null=True, blank=True)
    guests = models.IntegerField()
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.name} on {self.check_in}"
