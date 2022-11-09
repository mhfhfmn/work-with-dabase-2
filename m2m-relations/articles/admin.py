from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Section, ArticleSection


class ArticleSectionInlineFormset(BaseInlineFormSet):

    def clean(self):
        flag = 0

        for form in self.forms:

            if form.cleaned_data.get('DELETE'):
                continue

            if form.cleaned_data.get('is_main'):
                flag += 1

            if flag > 1:
                raise ValidationError('Возможно выбрать только 1 основной раздел.')

        if flag == 0:
            raise ValidationError('Добавьте основной раздел.')
        return super().clean()


class ArticleSectionInLine(admin.TabularInline):

    model = ArticleSection
    extra = 2
    formset = ArticleSectionInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    inlines = [ArticleSectionInLine]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    list_display = ['name']
