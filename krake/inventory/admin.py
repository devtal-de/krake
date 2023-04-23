from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.


admin.site.register(Item,ImportExportModelAdmin)
admin.site.register(Place,ImportExportModelAdmin)
admin.site.register(Owner,ImportExportModelAdmin)
admin.site.register(ForeignSystem,ImportExportModelAdmin)
admin.site.register(ForeignSystemLink,ImportExportModelAdmin)