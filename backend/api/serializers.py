from rest_framework import serializers
from .models import User, Medicine, Note, Document


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    username = serializers.CharField(min_length=8, max_length=20, write_only=True, allow_blank=True, required=False)
    class Meta:
        model = User
        fields = ['email', 'password', 'username'] #in the future, I shall add theme_default

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError({'email': 'Email is required.'})
        if not data.get('password'):
            raise serializers.ValidationError({'password': 'Password is required.'})
        return data

from .models import Note, Medicine

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'text', 'date', 'updated_at']
        read_only_fields = ['date', 'updated_at'] # I should remove one

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'title', 'description', 'dosage', 'date']

    def create(self, validated_data):
        validated_data.pop('user', None)
        user = self.context['request'].user
        return Medicine.objects.create(user=user, **validated_data)

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'document_file', 'uploaded_at']

    def validate_document_file(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        if file.content_type != 'application/pdf':
            raise serializers.ValidationError("File content type must be PDF.")
        return file