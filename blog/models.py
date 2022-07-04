from datetime import datetime
from unicodedata import name

from django.db import models

from autoslug import AutoSlugField


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_category_id_by_name(name: str) -> int:
        category, _ = Category.objects.get_or_create(name=name)
        return category.id


class Post(models.Model):
    DEFAULT_CATEGORY = "Uncategorised"

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    body = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    tags = models.ManyToManyField(to=Tag, related_name="posts", blank=True)
    category = models.ForeignKey(
        to=Category,
        related_name="posts",
        default=Category.get_category_id_by_name(DEFAULT_CATEGORY),
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
    )

    @property
    def excerpt(self):
        character_limit = 150
        if len(self.body) < character_limit:
            excerpt = self.body
        else:
            excerpt = self.body[:character_limit] + "..."

        return excerpt

    def save(self):
        self.updated_date = datetime.now()
        super().save()

    def publish(self):
        self.published_date = datetime.now()
        self.status = "published"
        self.save()

    def __str__(self):
        return self.title
