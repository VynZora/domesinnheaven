from django import forms
from django.utils import timezone

from .models import (
    Blog,
    Testimonial,
    Category,
    GalleryImage,
    ContactMessage,
    Activity,
    CampingPackage,
    Booking,
    DomeType,
)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):

    widget = MultipleFileInput

    def clean(self, data, initial=None):

        single_image_clean = super().clean

        if isinstance(data, (list, tuple)):

            return [
                single_image_clean(image, initial)
                for image in data
            ]

        if data:

            return [
                single_image_clean(data, initial)
            ]

        return []




# ============================================================
# DOME TYPE
# ============================================================

class DomeTypeForm(forms.ModelForm):

    images = MultipleImageField(
        required=False,
        label="Dome Images",
        widget=MultipleFileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        )
    )

    class Meta:

        model = DomeType

        fields = [
            "name",
            "description",
            "check_in",
            "check_out",
            "normal_price",
            "special_price",
            "package_items",
            "facilities",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter dome name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control rich-editor",
                    "rows": 5,
                    "placeholder": "Enter dome description",
                }
            ),

            "check_in": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "12:00 PM",
                }
            ),

            "check_out": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "11:00 AM",
                }
            ),

            "normal_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),

            "special_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),

            "package_items": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Enter one package item per line",
                }
            ),

            "facilities": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Enter one facility per line",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["package_items"].required = False
        self.fields["facilities"].required = False

        # Images required when creating,
        # optional when updating.
        if not self.instance or not self.instance.pk:
            self.fields["images"].required = True

# ============================================================
# BLOG
# ============================================================

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog

        fields = [
            "image",
            "title",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control rich-editor",
                }
            ),
        }


# ============================================================
# TESTIMONIAL
# ============================================================

class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial

        fields = [
            "name",
            "image",
            "review",
        ]


# ============================================================
# GALLERY CATEGORY
#
# IMPORTANT:
# Keep this Category.
# This is Gallery Category, NOT DomeCategory.
# ============================================================

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
        ]


# ============================================================
# GALLERY IMAGE
# ============================================================

class GalleryImageForm(forms.ModelForm):

    class Meta:
        model = GalleryImage

        fields = [
            "category",
            "title",
            "image",
        ]


# ============================================================
# CONTACT
# ============================================================

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "message",
        ]


# ============================================================
# ACTIVITY
# ============================================================

class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity

        fields = [
            "title",
            "description",
            "image",
            "duration",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control rich-editor",
                }
            ),
        }


# ============================================================
# CAMPING PACKAGE
# ============================================================

class CampingPackageForm(forms.ModelForm):

    class Meta:
        model = CampingPackage

        fields = [
            "name",
            "description",
            "main_image",
            "check_in",
            "check_out",
            "normal_price",
            "special_price",
            "package_items",
            "facilities",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control rich-editor",
                }
            ),
        }


# ============================================================
# BOOKING
#
# DomeCategory has been removed.
# User directly selects DomeType.
# ============================================================

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "name",
            "phone",
            "email",
            "guests",
            "check_in",
            "check_out",
            "dome_type",
            "jacuzzi_bathtub",
            "message",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your email",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),

            "check_in": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "check_out": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "dome_type": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_dome_type",
                }
            ),

            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Number of guests",
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Message (optional)",
                }
            ),
        }


    # ========================================================
    # DATE VALIDATION
    # ========================================================

    def clean(self):

        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        today = timezone.localdate()

        errors = {}

        # Check-in cannot be before today
        if check_in and check_in < today:
            errors["check_in"] = (
                "Check-in date cannot be in the past."
            )

        # Check-out must be after check-in
        if (
            check_in
            and check_out
            and check_out <= check_in
        ):
            errors["check_out"] = (
                "Check-out date must be after check-in date."
            )

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data