
from django.urls import path
from .views import NoteListCreateView,NoteListView, NoteRetrieveUpdateDestroyView, NoteShareView,NoteVersionHistoryView
urlpatterns = [
    path('create', NoteListCreateView.as_view(),name='create-new-note'),
    path('<int:pk>',NoteRetrieveUpdateDestroyView.as_view(),name='rud-on-notes'),
    path('',NoteListView.as_view(),name='get-all-notes'),
    path('<int:pk>/share',NoteShareView.as_view(),name='share-notes-with-other-users'),
    path('version-history/<int:id>',NoteVersionHistoryView.as_view(),name='get-notes-history')
]
