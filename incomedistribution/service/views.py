from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.db.models import Q
from rest_framework.response import Response
from django.db.utils import Error as DBError
from utils.exception import IDException
from . import serializers, models
from django.db.models import Sum
import pandas as pd
import logging

logger = logging.getLogger('server')


# Create your views here.

class DisplaySa4StateinfoView(GenericAPIView):
    """This POST API will return the relevant basic info of SA4 or State,
       after selecting a single object using the search bar on the left.
    """

    serializer_class = serializers.Sa4StateConfigSerializer

    def post(self, request):
        # Validate input parameters via serializer
        validated_data = self.get_validated_data(request.data)

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
    """This GET API will show all state types first drop-down list
    """

    def get(self, request):

        queryset = models.Sa4StateConfig.objects.values('state_id', 'state_name').distinct().order_by('state_id')
        state_info_list = [i for i in queryset]

        return Response(data=state_info_list)


class DisplayHouseholdCompositionListView(GenericAPIView):
    """This GET API will show all household composition types in the second drop-down list
    """

    def get(self, request):

        queryset = models.StateIncomeCounts.objects.values('household_composition').distinct().order_by('household_composition')
        household_composition_list = [i for i in queryset]

        return Response(data=household_composition_list)


class WeeklyHouseholdIncomeListView(GenericAPIView):
    """This GET API will show all income buckets types in the third drop-down list
    """

    def get(self, request):

        queryset = models.StateIncomeCounts.objects.values('weekly_household_income').distinct().order_by('weekly_household_income')
        household_composition_list = [i for i in queryset]

        return Response(data=household_composition_list)


class FilterView(GenericAPIView):
    """This POST API will show all income distribution information with combined filter search
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
    """This GET API Show all SA4 types in the fourth drop-down list
    """

    def get(self, request):

        queryset = models.Sa4StateConfig.objects.values('sa4_id', 'sa4_region_name').distinct().order_by('state_id')
        sa4_info_list = [i for i in queryset]

        return Response(data=sa4_info_list)


class Sa4StateCompareView(GenericAPIView):
    """This API will show comparison data about household counts proportion between sa4_region and state
        within the each pre-defined income bucket, after select a specific region.
    """

    def initial(self, request, *args, **kwargs):
        """Initiate to acquire the input parameters
        """
        super().initial(request, *args, **kwargs)

        self.sa4_region_name = request.data.get('sa4_region_name')
        self.state_name = self.fetch_state(request.data.get('sa4_region_name'))

    def post(self, request):

        # Compute count proportion data against sa4
        # Make ORM query: select sum(count) as totol_count where sa4_region_name=self.sa4_region_name groupby weekly_household_income
        qs_one_sa4 = models.Sa4IncomeCounts.objects.filter(sa4_region_name=self.sa4_region_name).values('weekly_household_income').order_by('weekly_household_income').annotate(total_count_one=Sum('count'))
        # Numerator of the counts proportion:   One region's total counts in each different income buckets
        df_one_sa4 = pd.DataFrame([i for i in qs_one_sa4])
        # Make ORM query: select sum(count) as totol_count groupby weekly_household_income
        qs_all_sa4 = models.Sa4IncomeCounts.objects.values('weekly_household_income').order_by('weekly_household_income').annotate(total_count_all=Sum('count'))
        # Denominator of the counts proportion: All regions' total counts in each different income buckets
        df_all_sa4 = pd.DataFrame([i for i in qs_all_sa4])
        df_merge_sa4 = pd.merge(df_one_sa4, df_all_sa4, on='weekly_household_income', how='inner')
        df_merge_sa4['sa4_proportion'] = df_merge_sa4.total_count_one/df_merge_sa4.total_count_all
        df_merge_sa4.drop(['total_count_one', 'total_count_all'], axis=1, inplace=True)
        sa4_prop_lst = df_merge_sa4.to_dict(orient='records')

        # Compute count proportion data against state
        # Make ORM query: select sum(count) as totol_count where state_name=self.state_name groupby weekly_household_income
        qs_one_state = models.StateIncomeCounts.objects.filter(state_name=self.state_name).values('weekly_household_income').order_by('weekly_household_income').annotate(total_count_one=Sum('count'))
        # Numerator of the counts proportion:   One state's total counts in each different income buckets
        df_one_state = pd.DataFrame([i for i in qs_one_state])

        # Make ORM query: select sum(count) as totol_count groupby weekly_household_income
        qs_all_state = models.StateIncomeCounts.objects.values('weekly_household_income').order_by('weekly_household_income').annotate(total_count_all=Sum('count'))
        # Denominator of the counts proportion: All states's total counts in each different income buckets
        df_all_state = pd.DataFrame([i for i in qs_all_state])
        df_merge_state = pd.merge(df_one_state, df_all_state, on='weekly_household_income', how='inner')
        df_merge_state['state_proportion'] = df_merge_state.total_count_one/df_merge_state.total_count_all
        df_merge_state.drop(['total_count_one', 'total_count_all'], axis=1, inplace=True)
        state_prop_lst = df_merge_state.to_dict(orient='records')

        # Restructure the result format to cater for front-end for further manipulation
        prop_compare_result = {self.sa4_region_name: sa4_prop_lst, self.state_name: state_prop_lst}

        return Response(data=prop_compare_result)

    def fetch_state(self, sa4_region_name):
        """Get corresponding state name by input sa4 region name
        """
        queryset = models.Sa4StateConfig.objects.filter(sa4_region_name=sa4_region_name).values_list('state_name', flat=True)
        if queryset.exists():
            state_name = [i for i in queryset][0]
            return state_name
        else:
            raise IDException(message="Sorry, could not find the associated state info of input region")


