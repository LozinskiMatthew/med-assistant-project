from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import User

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token["user_id"]
        except KeyError:
            return None

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        return user
