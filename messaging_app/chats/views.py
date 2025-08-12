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
        # Check if conversation_id is provided and user has access
        conversation_id = self.request.data.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if self.request.user not in conversation.participants.all():
                    return Response(
                        {'error': 'You are not a participant in this conversation'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                serializer.save(sender=self.request.user, conversation=conversation)
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        content = request.data.get('content')
        conversation_id = conversation.id
        
        # Check if user is participant in the conversation
        if request.user not in conversation.participants.all():
            return Response(
                {'error': 'You are not authorized to send messages to this conversation'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response({
            'message': serializer.data,
            'conversation_id': conversation_id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        participant_ids = request.data.get('participant_ids', [])
        
        if not participant_ids:
            return Response({'error': 'Participant IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if all participant_ids exist
        try:
            participants = User.objects.filter(id__in=participant_ids)
            if len(participants) != len(participant_ids):
                return Response(
                    {'error': 'One or more participant IDs are invalid'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            return Response(
                {'error': 'Invalid participant data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            conversation.participants.add(request.user)
            
            # Add other participants
            for participant in participants:
                conversation.participants.add(participant)
            
            return Response({
                'conversation': serializer.data,
                'conversation_id': conversation.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_conversation_messages(self, request):
        """Get messages for a specific conversation"""
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            
            # Check if user is participant
            if request.user not in conversation.participants.all():
                return Response(
                    {'error': 'You do not have access to this conversation'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
            serializer = MessageSerializer(messages, many=True)
            
            return Response({
                'conversation_id': conversation_id,
                'messages': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )