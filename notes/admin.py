from django.contrib import admin
from .models import Note
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Note,SimpleHistoryAdmin)


