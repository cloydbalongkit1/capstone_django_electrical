from django.contrib import admin
from .models import User, Calculations


admin.site.register(User)


@admin.register(Calculations)
class CircuitsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
