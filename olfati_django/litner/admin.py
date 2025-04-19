from django.contrib import admin

from . import models


@admin.register(models.LitnerModel)
class LinterModelAdmin(admin.ModelAdmin):
    filter_horizontal = ("paid_users",)
    list_display = ("title", "price", "myclass", "is_publish")
    list_select_related = ("myclass", )
    raw_id_fields = ("myclass", )
    list_filter = ("is_publish",)
    search_fields = ("title",)
    search_help_text = "برای جست و جو از فیلد (عنوان) استفاده کنید"
    actions = ("update_list_is_publish_false", "update_list_is_publish_true")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("paid_users").only(
            "title", "description", "price", "myclass__title", "data_created", "is_publish", "paid_users",
            "cover_image",
        )

    @admin.action(description='update list is publish, false')
    def update_list_is_publish_false(self, request, queryset):
        queryset.update(is_publish=False)

    @admin.action(description="update list is publish, true")
    def update_list_is_publish_true(self, request, queryset):
        queryset.update(is_publish=True)


@admin.register(models.MyLitnerclass)
class MyLinterClassAdmin(admin.ModelAdmin):
    raw_id_fields = ("author",)
    list_display = ("author", "title", "created_at", "is_publish")
    list_per_page = 20
    search_help_text = "برای جست و جو از فیلد (عنوان) استفاده کنید"
    search_fields = ("title",)
    list_editable = ("is_publish",)
    actions = ("update_list_is_publish_false", "update_list_is_publish_true")
    list_filter = ("is_publish",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "author__phone_number", "title", "is_publish", "cover_image", "study_field", "created_at",
            "updated_at"
        )

    @admin.action(description='update list is publish, false')
    def update_list_is_publish_false(self, request, queryset):
        queryset.update(is_publish=False)

    @admin.action(description="update list is publish, true")
    def update_list_is_publish_true(self, request, queryset):
        queryset.update(is_publish=True)


@admin.register(models.UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "box")
    list_select_related = ("user", "box")
    list_per_page = 20
    list_display = ("user", "box", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("user__phone_number",)
    search_help_text = "برای سرچ کردن کافی هست شماره موبایل کاربر رو وارد کنید"

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "user__phone_number", "box__question_text", "created_at", "updated_at", "status"
        )


@admin.register(models.UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LeitnerBox)
class LeitnerBoxAdmin(admin.ModelAdmin):
    raw_id_fields = ("linter",)
    list_display = ("linter", "box_number", "created_at", "is_active")
    list_per_page = 20
    list_editable = ("is_active",)
    actions = ("update_list_is_active_false", "update_list_is_active_true")
    list_select_related = ("linter__myclass",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "linter__title", "created_at", "is_active", 'box_number', "linter__myclass__title"
        )

    @admin.action(description='update list is active, false')
    def update_list_is_active_false(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="update list is active, true")
    def update_list_is_active_true(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(models.LinterFlashCart)
class LinterFlashCartAdmin(admin.ModelAdmin):
    raw_id_fields = ("box", )
    list_display = ("box", "is_active", "created_at")
    list_editable = ("is_active",)
    list_per_page = 20
    list_select_related = ("box",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "is_active", "box__box_number", "is_active", "created_at"
        )
