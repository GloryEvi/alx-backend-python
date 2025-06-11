import django_filters
from django.db import models
from .models import Message, User

class MessageFilter(django_filters.FilterSet):
    # Filter messages by specific users in conversation
    participant = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        method='filter_by_participant',
        help_text="Filter messages from conversations with this user"
    )
    
    # Filter messages within a time range
    created_after = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte',
        help_text="Messages created after this date/time"
    )
    
    created_before = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte',
        help_text="Messages created before this date/time"
    )
    
    # Filter by conversation
    conversation = django_filters.NumberFilter(
        field_name='conversation__id',
        help_text="Filter messages by conversation ID"
    )
    
    class Meta:
        model = Message
        fields = ['participant', 'created_after', 'created_before', 'conversation']
    
    def filter_by_participant(self, queryset, name, value):
        """Filter messages from conversations that include the specified user"""
        if value:
            return queryset.filter(conversation__participants=value)
        return queryset