from django.contrib import admin

from .models import Note, Label


class NoteModelAdmin(admin.ModelAdmin):
    list_display = ["note_title", "author", "public", "archived", "updated", "timestamp"]
    # list_display_links = ["updated"]
    # list_editable = ["title"]
    list_filter = ["updated", "timestamp", "public", "archived"]
    search_fields = ["note_title", "note_text", "author"]

    class Meta:
        model = Note


class LabelModelAdmin(admin.ModelAdmin):
    list_display = ["text", "background_color", "user", "text_color"]
    search_fields = ["text", "user"]
    list_filter = ["user"]

    class Meta:
        model = Note

admin.site.register(Note, NoteModelAdmin)
admin.site.register(Label, LabelModelAdmin)
