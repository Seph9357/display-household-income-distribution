from rest_framework import serializers
from . import models

class Sa4StateConfigSerializer(serializers.Serializer):
    """Data type validation
    """
    sa4_id = serializers.IntegerField(required=False)
    sa4_region_name = serializers.CharField(required=False)
    state_id = serializers.IntegerField(required=False)
    state_name = serializers.CharField(required=False)

    class Meta:
        model = models.Sa4StateConfig
        fields = '__all__'