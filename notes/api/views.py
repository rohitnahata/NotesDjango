from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from notes.models import Note
from .permissions import IsOwnerOrReadOnly
from .serializers import NoteDetailSerializer, NoteListSerializer, NoteComposeUpdateSerializer


class NoteComposeAPIView(CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteComposeUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_anonymous:
            serializer.save(author=self.request.user)
        else:
            pass


class NoteListAPIView(ListAPIView):
    serializer_class = NoteListSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self):
        queryset = Note.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(note_text__icontains=query) |
                Q(note_title__icontains=query) |
                Q(author__username__icontains=query) |
                Q(labels__text__icontains=query)
            ).distinct()
        print(queryset)
        return queryset


class NoteEditAPIView(RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteComposeUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        if not self.request.user.is_anonymous:
            serializer.save(author=self.request.user)
        else:
            pass


class NoteDeleteAPIView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteListSerializer


class NoteDetailAPIView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer
    # lookup_field = "slug"
