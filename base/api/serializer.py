from rest_framework import serializers
from base.models import Revenue
from django.contrib.auth import get_user_model

class SerializerRevenue(serializers.ModelSerializer):
    revenue_set = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name_revenue'
    )
    class Meta:
        model = get_user_model()

        fields = [
            'name',
            'revenue_set'
        ]