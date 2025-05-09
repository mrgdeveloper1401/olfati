from rest_framework import permissions


# پرمیشن برای سوپر یوزر
# class IsSuperUserOrStaff(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.method in SAFE_METHODS and
#                     request.user and
#                     request.user.is_staff and
#                     request.user and
#                     request.user.is_superuser)


# پرمیشن برای چک کردن احراز هویت کاربر
# class IsAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return bool(request.user.is_authenticated or request.user.is_superuser)

# #پرمیشن برای چک کردن پرداخت کاربر
# class HasPurchasedAccess(BasePermission):
#     def has_permission(self, request,view):
#         if request.method in SAFE_METHODS and request.user.is_authenticated:
#          return True
#         try:
#             payment=Payment.objects.get(user=request.user.id)
#         except Payment.DoesNotExist:
#             return False
#         return getattr(payment,'has_access',True)


class IsOwnerOrReadOnlyLinterModel(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(obj.myclass.author == request.user)


class IsOwnerOrReadOnlyLinterClass(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.author == request.user)


class IsOwnerOrReadOnlyLinterFlashCart(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(obj.season.myclass.author == request.user)
