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

