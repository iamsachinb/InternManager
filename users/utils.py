import pandas as pd
from .forms import CustomUserCreationForm
from .models import Profile


def createAccounts(df):

    for row in df.values:
        name = row[0]
        email = row[1]
        regno = row[2]
        username = str(regno) 
        
        ss = str(row[3]).split(maxsplit=1)
        password = ss[0]

        form = CustomUserCreationForm({
            'first_name': name,
            'username': username,
            'email': email,
            'password1': password,
            'password2': password,
        })

        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=user.first_name,
                regno = regno
            )

            


        
        




