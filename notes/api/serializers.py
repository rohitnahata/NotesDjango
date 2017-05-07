from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from notes.models import Note

post_detail_url = HyperlinkedIdentityField(
    view_name='notes_api:detail',
    # lookup_field='slug'
)
post_delete_url = HyperlinkedIdentityField(
    view_name='notes_api:delete',
    # lookup_field='slug'
)


class NoteComposeUpdateSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = [
            # "id",
            "note_title",
            "note_text",
            # "slug",
            # "author",
            "pub_date",
            "timestamp"
        ]


class NoteListSerializer(ModelSerializer):
    detail = post_detail_url
    author = SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "detail",
            "id",
            "note_title",
            "note_text",
            # "slug",
            "author"
        ]

    def get_author(self, obj):
        return obj.author.username


class NoteDetailSerializer(ModelSerializer):
    delete = post_delete_url
    author = SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "id",
            "note_title",
            "note_text",
            "slug",
            "author",
            "public",
            "labels",
            "delete"
        ]

    def get_author(self, obj):
        return obj.author.username
