from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    
    def get_queryset(self):
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations).order_by('-timestamp')
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        participant_ids = request.data.get('participant_ids', [])
        
        if not participant_ids:
            return Response({'error': 'Participant IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            conversation.participants.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)