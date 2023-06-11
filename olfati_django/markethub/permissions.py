from rest_framework.permissions import BasePermission, SAFE_METHODS,IsAuthenticated
from .models import Payment



#پرمیشن برای سوپر یوزر
class IsSuperUserOrStaff(BasePermission):
    def has_permission(self, request, view):
        return bool (request.method in SAFE_METHODS and 
        request.user and 
        request.user.is_staff and 
        request.user and 
        request.user.is_superuser)
    
#پرمیشن برای چک کردن احراز هویت کاربر
class IsAuthenticated(BasePermission):
   def has_permission(self, request, view):
      if request.method in SAFE_METHODS:
         return True
      return bool(request.user.is_authenticated or request.user.is_superuser)
    


#پرمیشن برای چک کردن پرداخت کاربر

class HasPurchasedAccess(BasePermission):
    def has_object_permission(self, request,view):
        return request.user.is_authenticated and request.user.Payment.has_access  
    






