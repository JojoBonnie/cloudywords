from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mfa_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class UserCredit(models.Model):
    """Track user credits for AI-generated word clouds"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credits')
    credits_remaining = models.IntegerField(default=3)  # Free users get 3 free uses
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.credits_remaining} credits"


class WordCloud(models.Model):
    """Stores word cloud data and settings"""
    FONT_CHOICES = [
        ('arial', 'Arial'),
        ('times', 'Times New Roman'),
        ('courier', 'Courier New'),
        ('verdana', 'Verdana'),
        ('georgia', 'Georgia'),
        ('trebuchet', 'Trebuchet MS'),
        ('comic', 'Comic Sans MS'),
    ]

    COLOR_SCHEME_CHOICES = [
        ('Default', 'Default'),
        ('Blues', 'Blues'),
        ('Reds', 'Reds'),
        ('Greens', 'Greens'),
        ('Purples', 'Purples'),
        ('Oranges', 'Oranges'),
        ('Greys', 'Greys'),
        ('Rainbow', 'Rainbow'),
        # Optionally, add more valid Matplotlib colormaps here
    ]

    ORIENTATION_CHOICES = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('random', 'Random'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='word_clouds')
    title = models.CharField(max_length=100)
    input_text = models.TextField()
    is_ai_generated = models.BooleanField(default=False)

    # Customization options
    width = models.PositiveIntegerField(default=800)
    height = models.PositiveIntegerField(default=400)
    font = models.CharField(max_length=20, choices=FONT_CHOICES, default='arial')
    color_scheme = models.CharField(max_length=20, choices=COLOR_SCHEME_CHOICES, default='Default')
    background_color = models.CharField(max_length=20, default='white')
    max_words = models.PositiveIntegerField(default=200)
    word_density = models.PositiveIntegerField(default=80)  # Scale of 1–100
    orientation = models.CharField(max_length=20, choices=ORIENTATION_CHOICES, default='random')

    # Storage details
    image_url = models.URLField(blank=True, null=True)
    svg_url = models.URLField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


# Signal handlers to create profile and credits when a user is created
@receiver(post_save, sender=User)
def create_user_profile_and_credits(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserCredit.objects.create(user=instance)
