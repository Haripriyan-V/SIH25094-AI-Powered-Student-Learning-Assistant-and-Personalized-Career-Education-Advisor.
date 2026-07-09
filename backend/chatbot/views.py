from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer, ChatSessionListSerializer,
    ChatMessageSerializer, SendMessageSerializer,
)


def generate_ai_reply(user, message_text):
    """
    Placeholder AI response generator.

    This is a stand-in for the real AI/LLM integration that will be wired
    up in the AI module (Phase 3). Keeping the call isolated in a single
    function makes it trivial to swap in a real model/API call later
    without touching any view logic.
    """
    return (
        f"Thanks for your message, {user.first_name or user.username}! "
        f"I'm your AI learning assistant. You asked about: \"{message_text[:200]}\". "
        f"A full AI-powered response will be available once the recommendation "
        f"engine is integrated."
    )


class ChatSessionViewSet(viewsets.ModelViewSet):
    """A student's own chat sessions with the AI assistant."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(student=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSessionListSerializer
        return ChatSessionSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        POST /api/chatbot/sessions/{id}/send_message/
        Body: {"message": "..."}
        Stores the user's message, generates an AI reply, stores it too,
        and returns both messages.
        """
        session = self.get_object()
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['message']

        user_message = ChatMessage.objects.create(
            session=session, sender=ChatMessage.Sender.USER, message=text,
        )
        ai_reply_text = generate_ai_reply(request.user, text)
        ai_message = ChatMessage.objects.create(
            session=session, sender=ChatMessage.Sender.ASSISTANT, message=ai_reply_text,
        )
        session.save(update_fields=['updated_at'])  # bump updated_at via auto_now

        return Response(
            {
                'user_message': ChatMessageSerializer(user_message).data,
                'assistant_message': ChatMessageSerializer(ai_message).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only access to individual messages (mainly for filtering/debugging)."""
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(session__student=self.request.user)
