from django import forms
from django.contrib import admin, messages
from .models import Post, Category, Pets, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ['title', 'text', 'category', 'photo', 'video']  # поля формы создания и редакции
    list_display = ('id', 'title', 'time', 'is_published', 'category')  # поля отображаемые в списке объектов
    list_display_links = ('id', 'title')  # поля линк
    ordering = ['-time', 'title']  # сортировка
    list_editable = ('is_published',)  # разрешение редактировать прям на странице списка
    list_per_page = 10  # пагинация
    actions = ['set_published', 'set_draft']  # доп действия
    list_filter = ['category__name', 'is_published']  # фильтрация по полям
    readonly_fields = []  # поля неизменяемое (видное в форме)

    def save_model(self, request, obj, form, change):
        if not change:  # Только при создании новой записи
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        # Получаем стандартную форму
        form = super().get_form(request, obj, **kwargs)
        if 'author' in form.base_fields:
            form.base_fields['author'].disabled = True
        # Явно добавляем поле slug, даже если editable=False
        form.base_fields['slug'] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
        )
        return form

    # добавление пользовательского поля в админку
    # @admin.display(description='Имя поля', ordering='сортировка по полю из модели')
    # def my_func(self, post: Post):
    #     return f'описание поля {len(post.text)} и тд.'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с пуюликации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Pets)
admin.site.register(Comment)
