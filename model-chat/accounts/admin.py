from django.contrib import admin

from accounts.models import User

class all_objects(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.all_objects.get_queryset()

admin.site.register(User, all_objects)