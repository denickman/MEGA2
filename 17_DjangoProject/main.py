# django-admin startproject mysite . - will create a dirctory with py files + manage.py
# python manage.py startapp job_app - will create another directory job_app
# go to mysite - settings - INSTALLED_APPS and add new string 'job_app'

# python manage.py runserver

"""

then go to job_app -> models -> create your own model

class Form(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    occupation = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'




after that go to job_app -> views -> create your own view
def index(request):
    return render(request, "index.html")


after that create iin job_app create templates subfolder for your html pages
than in job_app create urls.py


then go to mysite directory - urls
find urlpatterns = [
    path('admin/', admin.site.urls),
]
and add   path('', include('job_app.urls')), как бы соединяешь урлы из папки job_app с этими 


"""

