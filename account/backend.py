from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **extra_fields):
        if email == None or password == None:
            return 
        try:
            user = UserModel.objects.get(email = email)
            self.block_user(user, request)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return 
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        elif user.check_password(password) == False and user.number_of_attempts > 0:
            user.number_of_attempts -= 1
            user.save()
            return

    
    def block_user(self, user, request):
        if user.number_of_attempts == 0 and user.is_active:
            user.is_active = False 
            user.save()
            messages.error(request, 'O usuário foi bloqueado por inúmeras tentativas para realizar o login')