from rest_framework import serializers
from .models import User, Conversation, Message


from rest_framework.serializers import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'is_online', 'last_seen']
        read_only_fields = ['id', 'last_seen']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'conversation', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp', 'sender']
    
    def validate_content(self, value):
        if not value.strip():
            raise ValidationError("Message content cannot be empty.")
        if len(value) > 1000:
            raise ValidationError("Message content cannot exceed 1000 characters.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participant_ids', 'messages', 'last_message', 'unread_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        return obj.messages.filter(is_read=False).count()
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        if participant_ids:
            conversation.participants.set(participant_ids)
        return conversation