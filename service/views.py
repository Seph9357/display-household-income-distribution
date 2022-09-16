from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.db.models import Q
from rest_framework.response import Response
from django.db.utils import Error as DBError
from utils.exception import IDException

from . import serializers, models

import logging

logger = logging.getLogger('server')


# Create your views here.

class DisplaySa4StateinfoView(GenericAPIView):
    """After selecting a single object using the search bar on the left,
       this API will return the relevant basic info of SA4 or State.
    """

    serializer_class = serializers.Sa4StateConfigSerializer

    def post(self, request):
        # Validate input parameters
        validated_data = self.get_validated_data(request.data)
        print(validated_data)
        try:
            sa4_region_name = validated_data["sa4_region_name"]
            # Make ORM query
            sa4_state_queryset = models.Sa4StateConfig.objects.filter(sa4_region_name=sa4_region_name).values()
        except:
            pass

        try:
            state_name = validated_data["state_name"]
            # Make ORM query
            sa4_state_queryset = models.Sa4StateConfig.objects.filter(state_name=state_name).values()
        except:
            pass

        if sa4_state_queryset.exists():
            sa4_state_info = [i for i in sa4_state_queryset]
            return Response(data=sa4_state_info)
        else:
            raise IDException(message="Sorry, the input location not in our database")

    def get_validated_data(self, data) -> dict:
        """Validate data type via pre-defined serializer
        """
        serializer_cls = self.get_serializer_class()
        serializer = serializer_cls(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data



class DisplayStateListView(GenericAPIView):
    """show all state information first drop-down list
    """

    def get(self, request):


        queryset = models.Sa4StateConfig.objects.values('state_id','state_name').distinct().order_by('state_id')
        state_info_list = [i for i in queryset]

        return Response(data=state_info_list)


class DisplayHouseholdCompositionListView(GenericAPIView):
    """show all state information first drop-down list
    """

    def get(self, request):


        queryset = models.StateIncomeCounts.objects.values('household_composition').distinct().order_by('household_composition')
        household_composition_list = [i for i in queryset]

        return Response(data=household_composition_list)


class WeeklyHouseholdIncomeListView(GenericAPIView):
    """show all state information first drop-down list
    """

    def get(self, request):


        queryset = models.StateIncomeCounts.objects.values('weekly_household_income').distinct().order_by('weekly_household_income')
        household_composition_list = [i for i in queryset]

        return Response(data=household_composition_list)
