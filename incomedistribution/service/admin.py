from django.contrib import admin
from import_export import admin as resourceadmin, resources
from . import models

# Register your models here.

class Sa4StateConfigResource(resources.ModelResource):
    class Meta:
        model = models.Sa4StateConfig

@admin.register(models.Sa4StateConfig)
class Sa4StateConfigAdmin(resourceadmin.ImportExportModelAdmin):
    list_display = ('sa4_id', 'sa4_region_name', 'state_id', 'state_name')
    search_fields = ('sa4_id', 'sa4_region_name', 'state_id', 'state_name')
    resource_class = Sa4StateConfigResource


