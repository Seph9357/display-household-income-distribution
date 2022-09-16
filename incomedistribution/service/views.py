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
    """Show all state types first drop-down list
    """

    def get(self, request):

        queryset = models.Sa4StateConfig.objects.values('state_id', 'state_name').distinct().order_by('state_id')
        state_info_list = [i for i in queryset]

        return Response(data=state_info_list)


class DisplayHouseholdCompositionListView(GenericAPIView):
    """Show all household composition types in the second drop-down list
    """

    def get(self, request):

        queryset = models.StateIncomeCounts.objects.values('household_composition').distinct().order_by('household_composition')
        household_composition_list = [i for i in queryset]

        return Response(data=household_composition_list)


class WeeklyHouseholdIncomeListView(GenericAPIView):
    """Show all income buckets types in the third drop-down list
    """

    def get(self, request):

        queryset = models.StateIncomeCounts.objects.values('weekly_household_income').distinct().order_by('weekly_household_income')
        household_composition_list = [i for i in queryset]

        return Response(data=household_composition_list)


class FilterView(GenericAPIView):
    """This API will show all income distribution information with combined filter search
        by state, household composition, Weekly Household Income
    """

    def initial(self, request, *args, **kwargs):
        """Initiate to acquire the input parameters
        """
        super().initial(request, *args, **kwargs)

        all_state_list = [i for i in models.Sa4StateConfig.objects.values_list('state_name', flat=True).distinct()]
        all_household_composition_list = [i for i in models.StateIncomeCounts.objects.values_list('household_composition', flat=True).distinct()]
        all_weekly_household_income_list = [i for i in models.StateIncomeCounts.objects.values_list('weekly_household_income', flat=True).distinct()]

        # Following decisions on value assignment will cover the the scenario that
        # clients do not choose one or more selection field.
        # Then by default, if there is no selection, it essentially means select all against this field.
        self.state_name = [i for i in [request.data.get("state_name")] if i != ''] or all_state_list
        self.household_composition = [i for i in [request.data.get("household_composition")] if i != ''] or all_household_composition_list
        self.weekly_household_income = [i for i in [request.data.get("weekly_household_income")] if i != ''] or all_weekly_household_income_list


    def post(self, request):
        # make ORM query
        queryset = models.Sa4IncomeCounts.objects.filter(
            Q(sa4__state_name__in=self.state_name) & Q(household_composition__in=self.household_composition) & Q(
                weekly_household_income__in=self.weekly_household_income)).values(
            'sa4_region_name', 'sa4__state_name', 'household_composition', 'weekly_household_income', 'count')

        if queryset.exists():
            data = [i for i in queryset]
            return Response(data=data)
        else:
            raise IDException(message="Sorry, no results after combined filter search")


class DisplaySA4ListView(GenericAPIView):
    """Show all SA4 types in the fourth drop-down list
    """

    def get(self, request):

        queryset = models.Sa4StateConfig.objects.values('sa4_id', 'sa4_region_name').distinct().order_by('state_id')
        sa4_info_list = [i for i in queryset]

        return Response(data=sa4_info_list)