from django import forms
from django.utils import timezone
from .models import Blog, Testimonial, Category, GalleryImage, ContactMessage, Activity, CampingPackage, Booking, DomeCategory, DomeType


class DomeCategoryForm(forms.ModelForm):
    class Meta:
        model = DomeCategory
        fields = ["name", "image"]


class DomeTypeForm(forms.ModelForm):
    class Meta:
        model = DomeType
        fields = [
            "category", "name", "description", "main_image", "check_in", "check_out",
            "normal_price", "special_price",
            "package_items", "facilities"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control rich-editor"}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image", "title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control rich-editor"}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "image", "review"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["category", "title", "image"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "phone", "email", "message"]

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "description", "image", "duration"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control rich-editor"}),
        }


class CampingPackageForm(forms.ModelForm):
    class Meta:
        model = CampingPackage
        fields = [
            "name", "description", "main_image", "check_in", "check_out",
            "normal_price", "special_price",
            "package_items", "facilities"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control rich-editor"}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["name", "email", "phone", "check_in", "check_out", "dome_category", "dome_type", "guests", "message"]
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dome_category': forms.Select(attrs={'class': 'form-control', 'id': 'id_dome_category'}),
            'dome_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_dome_type'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        today = timezone.localdate()

        errors = {}
        if check_in and check_in < today:
            errors["check_in"] = "Check-in date cannot be in the past."

        if check_in and check_out and check_out <= check_in:
            errors["check_out"] = "Check-out date must be after check-in date."

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
