from rest_framework import serializers
from .models import Note
from notes_backend.serializers import UserSerializer

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__' #['id', 'title', 'content', 'owner', 'shared_users', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at','shared_users']
        extra_kwargs = {'shared_users': {'required': False, 'default': []}}

    def create(self, validated_data):
        #if shared users are while creating notes
        shared_users = validated_data.pop('shared_users', [])
        note = Note.objects.create(**validated_data)
        note.shared_users.add(note.owner)

        # add the other shared_users if any
        note.shared_users.add(*shared_users)
        return note
    
    def validate(self, data):
        
        return data

class NoteVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']