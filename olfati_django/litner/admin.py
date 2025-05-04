from django.contrib import admin

from . import models


@admin.register(models.LinterModel)
class LinterModelAdmin(admin.ModelAdmin):
    filter_horizontal = ("paid_users",)
    list_display = ("title", "id", "price", "myclass", "myclass_id", "paid_user_count", "is_sale")
    list_select_related = ("myclass", )
    list_editable = ("is_sale",)
    raw_id_fields = ("myclass",)
    search_fields = ("title",)
    search_help_text = "برای جست و جو از فیلد (عنوان) استفاده کنید"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("paid_users").only(
            "title", "description", "price", "myclass__title", "paid_users", "cover_image", 'is_sale'
        )


@admin.register(models.MyLinterClass)
class MyLinterClassAdmin(admin.ModelAdmin):
    # raw_id_fields = ("author",)
    list_display = ("author_full_name", "id", "title", "created_at")
    list_per_page = 20
    search_help_text = "برای جست و جو از فیلد (عنوان) استفاده کنید"
    search_fields = ("title",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "author__phone_number", "title", "cover_image", "study_field", "created_at", "updated_at")

    def author_full_name(self, obj):
        return obj.author.get_full_name()


@admin.register(models.UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "flash_cart", "is_correct")
    raw_id_fields = ("flash_cart", "user")
    list_select_related = ("flash_cart", "user")
    list_per_page = 20
    search_help_text = "برای سرچ کردن کافی هست شماره موبایل کاربر رو وارد کنید"


# @admin.register(models.UserProgress)
# class UserProgressAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.LeitnerBox)
class LeitnerBoxAdmin(admin.ModelAdmin):
    raw_id_fields = ("linter",)
    list_display = ("linter", "id", "linter_id", "box_number", "created_at")
    list_per_page = 20
    actions = ("update_list_is_active_false", "update_list_is_active_true")
    list_select_related = ("linter__myclass",)
    search_fields = ("linter__title",)
    search_help_text = "برای سرچ کردن میتوانید از عنوان فصل استفاده کنید"
    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "linter__title", "created_at", 'box_number', "linter__myclass__title"
        )

    # @admin.action(description='update list is active, false')
    # def update_list_is_active_false(self, request, queryset):
    #     queryset.update(is_active=False)
    #
    # @admin.action(description="update list is active, true")
    # def update_list_is_active_true(self, request, queryset):
    #     queryset.update(is_active=True)


@admin.register(models.LinterFlashCart)
class LinterFlashCartAdmin(admin.ModelAdmin):
    list_display = ("box", "id", "season", "is_active", "created_at")
    list_editable = ("is_active",)
    list_per_page = 20
    # raw_id_fields = ("season",)
    list_select_related = ('season',)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "is_active", "box", "is_active", "created_at", "season__title"
        )
