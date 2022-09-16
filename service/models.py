from django.db import models

# Create your models here.
class Sa4StateConfig(models.Model):
    """table stores SA4 and State basic information
    """
    sa4_id = models.IntegerField(primary_key=True)
    sa4_region_name = models.CharField('sa4_region_name', max_length=64, null=False, blank=False, db_index=True)
    state_id = models.IntegerField('state_id', null=False, blank=False, db_index=True)
    state_name = models.CharField('state_name', max_length=64, null=False, blank=False, db_index=True)

    class Meta:
        db_table = 'config_sa4_state'
        verbose_name = 'sa4_state_info'
        verbose_name_plural = verbose_name


class StateIncomeCounts(models.Model):
    """table stores household counts broken down by State, Household Composition and
       Weekly Household Income Bracket
    """
    state_id = models.IntegerField("state_id", null=False, blank=False, db_index=True)
    state_name = models.CharField('state_name', max_length=64, null=False, blank=False, db_index=True)
    household_composition = models.CharField('household_composition', max_length=64, null=False, blank=False, db_index=True)
    weekly_household_income = models.CharField('weekly_household_income', max_length=64, null=False, blank=False, db_index=True)
    count = models.IntegerField('count', null=True, blank=True)

    class Meta:
        db_table = 'counts_state_income'
        verbose_name = 'state_income_distribution'
        verbose_name_plural = verbose_name



