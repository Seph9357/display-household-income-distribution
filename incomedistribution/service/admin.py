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


class StateIncomeCountsResource(resources.ModelResource):
    class Meta:
        model = models.StateIncomeCounts

@admin.register(models.StateIncomeCounts)
class StateIncomeCountsAdmin(resourceadmin.ImportExportModelAdmin):
    list_display = ('id', 'state_id', 'state_name', 'household_composition', 'weekly_household_income','count')
    search_fields = ('state_id', 'state_name', 'household_composition', 'weekly_household_income')
    resource_class = StateIncomeCountsResource


class Sa4IncomeCountsResource(resources.ModelResource):
    class Meta:
        model = models.Sa4IncomeCounts

@admin.register(models.Sa4IncomeCounts)
class Sa4IncomeCountsAdmin(resourceadmin.ImportExportModelAdmin):
    list_display = ('id', 'sa4_id', 'sa4_region_name', 'state_id',  'household_composition', 'weekly_household_income', 'count')
    search_fields = ('sa4_id', 'sa4_region_name', 'state_id', 'household_composition', 'weekly_household_income')
    resource_class = Sa4IncomeCountsResource