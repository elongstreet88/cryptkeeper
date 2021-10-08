app_name=cryptkeeper
django-admin startproject main
cd main
python manage.py migrate
python manage.py createsuperuser

python manage.py startapp $app_name

tee ./$app_name/views.py << END
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the index.")
END


tee ./$app_name/urls.py << END
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
END


sed -i "s/admin.site.urls),/replace_string/" ./urls.py

#Add site:
#Domain name: 127.0.0.1:8000
#Display name: 127.0.0.1:8000

#Add social app
#Provider: Google
#Name: Google API
#Client id: (generated at the end of Google API setup)
#Secret key: (generated at the end of Google API setup)
#Site: 127.0.0.1:8000