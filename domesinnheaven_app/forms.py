import re
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

# ============================================================
# BOOKING FORM + COMPLETE VALIDATION
# ============================================================

import re

from django import forms
from django.utils import timezone

from .models import Booking


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
            "message",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. John Doe",
                    "minlength": "2",
                    "maxlength": "100",
                    "autocomplete": "name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. +91 9946 280 626",
                    "maxlength": "18",
                    "autocomplete": "tel",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. john@example.com",
                    "maxlength": "254",
                    "autocomplete": "email",
                }
            ),

            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 2",
                    "min": "1",
                    "max": "20",
                    "step": "1",
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

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": "1000",
                    "placeholder": "Tell us anything we should know...",
                }
            ),
        }


    # ========================================================
    # REQUIRED / OPTIONAL FIELDS
    # ========================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required fields
        self.fields["name"].required = True
        self.fields["phone"].required = True
        self.fields["email"].required = True
        self.fields["guests"].required = True
        self.fields["check_in"].required = True
        self.fields["check_out"].required = True
        self.fields["dome_type"].required = True

        # Optional field
        self.fields["message"].required = False

        # Dome dropdown
        self.fields["dome_type"].queryset = (
            self.fields["dome_type"]
            .queryset
            .order_by("name")
        )

        self.fields["dome_type"].empty_label = "Select Dome Type"


    # ========================================================
    # NAME VALIDATION
    # ========================================================

    def clean_name(self):

        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise forms.ValidationError(
                "Please enter your name."
            )

        if len(name) < 2:
            raise forms.ValidationError(
                "Name must contain at least 2 characters."
            )

        if len(name) > 100:
            raise forms.ValidationError(
                "Name cannot exceed 100 characters."
            )

        # Allow letters, spaces, dot, apostrophe and hyphen
        if not re.fullmatch(
            r"[A-Za-zÀ-ÖØ-öø-ÿ.' -]+",
            name
        ):
            raise forms.ValidationError(
                "Please enter a valid name. "
                "Numbers and special symbols are not allowed."
            )

        return name


    # ========================================================
    # PHONE VALIDATION
    # ========================================================

    def clean_phone(self):

        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            raise forms.ValidationError(
                "Please enter your phone number."
            )

        # Remove spaces, brackets and hyphens
        cleaned_phone = re.sub(
            r"[\s()-]",
            "",
            phone
        )

        # Accepted examples:
        # 9946280626
        # 919946280626
        # +919946280626
        # +91 9946 280 626

        if not re.fullmatch(
            r"\+?\d{10,15}",
            cleaned_phone
        ):
            raise forms.ValidationError(
                "Please enter a valid phone number "
                "with 10 to 15 digits."
            )

        return phone


    # ========================================================
    # EMAIL VALIDATION
    # ========================================================

    def clean_email(self):

        email = self.cleaned_data.get(
            "email",
            ""
        ).strip().lower()

        if not email:
            raise forms.ValidationError(
                "Please enter your email address."
            )

        # Django EmailField validates email format.
        return email


    # ========================================================
    # NUMBER OF GUESTS VALIDATION
    # ========================================================

    def clean_guests(self):

        guests = self.cleaned_data.get("guests")

        if guests is None:
            raise forms.ValidationError(
                "Please enter the number of guests."
            )

        if guests < 1:
            raise forms.ValidationError(
                "At least 1 guest is required."
            )

        if guests > 20:
            raise forms.ValidationError(
                "Maximum 20 guests are allowed."
            )

        return guests


    # ========================================================
    # DOME TYPE VALIDATION
    # ========================================================

    def clean_dome_type(self):

        dome_type = self.cleaned_data.get(
            "dome_type"
        )

        if not dome_type:
            raise forms.ValidationError(
                "Please select a dome type."
            )

        return dome_type


    # ========================================================
    # MESSAGE VALIDATION
    # ========================================================

    def clean_message(self):

        message = self.cleaned_data.get(
            "message",
            ""
        ).strip()

        if len(message) > 1000:
            raise forms.ValidationError(
                "Special request cannot exceed "
                "1000 characters."
            )

        return message


    # ========================================================
    # CHECK-IN / CHECK-OUT VALIDATION
    # ========================================================

    def clean(self):

        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        today = timezone.localdate()

        # Check-in cannot be in the past
        if check_in and check_in < today:

            self.add_error(
                "check_in",
                "Check-in date cannot be in the past."
            )

        # Check-out must be after check-in
        if (
            check_in
            and check_out
            and check_out <= check_in
        ):

            self.add_error(
                "check_out",
                "Check-out date must be after check-in date."
            )

        return cleaned_data