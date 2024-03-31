from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer,NoteVersionSerializer
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class NoteListView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]

class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user == obj.owner or self.request.user in obj.shared_users.all():
            return obj
        else:
            raise PermissionDenied('You do not have permission to access this note.')
 

class NoteShareView(generics.GenericAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
      
        note = self.get_object()
        
        if self.request.user == note.owner:
           
            users = request.data.get('users', [])
            
            if users and isinstance(users, list):
                
                for user in users:
                   
                    try:
                        #can shared with users by giving there username or email
                        user = User.objects.get(username=user) or User.objects.get(email=user)
                       
                        note.shared_users.add(user)
                    except User.DoesNotExist:
                      
                        return Response({'error': f'User {user} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
              
                note.save()
            
                return Response({'message': f'Note {note.id} shared successfully with {users}.'}, status=status.HTTP_200_OK)
            else:
               
                return Response({'error': 'Users must be a list of usernames or emails.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied('You do not have permission to share this note.')


class NoteVersionHistoryView(generics.ListAPIView):
    serializer_class = NoteVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            note = Note.objects.get(id=self.kwargs['id'])
            if self.request.user == note.owner or self.request.user in note.shared_users.all():
                return note.history.all()
            else:
                raise PermissionDenied('You do not have permission to access this note.')
        except Note.DoesNotExist as e:
            raise  NotFound(str(e))
