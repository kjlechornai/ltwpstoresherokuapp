from django.contrib import admin
from .models import Item, Category, Location, Shelf, Department, Project, Receive, Issue, Image, ReturnToSupplier, ReturnToStore
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = 'Stores administration'

class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ( 'name',)
    list_filter = ('category', 'sub_category')
    class Meta:
        model = Item

class LocationAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    class Meta:
        model = Location

class CategoryAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    class Meta:
        model = Category

class DepartmentAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    class Meta:
        model = Department

class ProjectAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    class Meta:
        model = Project

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shelf)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Receive)
admin.site.register(Issue)
admin.site.register(Image)
admin.site.register(Location, LocationAdmin)
admin.site.register(ReturnToSupplier)
admin.site.register(ReturnToStore)



