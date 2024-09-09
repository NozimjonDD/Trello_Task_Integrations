from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is deleted"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Deleted at"))

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class NewsCategory(BaseModel):
    class Meta:
        db_table = "news_category"
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    ordering = models.IntegerField(default=0, verbose_name=_("Ordering"))

    def __str__(self):
        return f"{self.title}"


class News(BaseModel):
    class Meta:
        db_table = "news"
        verbose_name = _("News")
        verbose_name_plural = _("News")

    category = models.ForeignKey(
        to="NewsCategory", on_delete=models.CASCADE, verbose_name=_("Category"), related_name="news"
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to="common/news/", verbose_name=_("Image"))
    content = RichTextUploadingField(verbose_name=_("Content"))

    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Published at"), default=timezone.now)

    def __str__(self):
        return f"{self.title}"
