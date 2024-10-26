from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('professor', 'Professor')])
    school_year = models.CharField(max_length=1, choices=[('1', '1ère année'), ('2', '2ème année'), ('3', '3ème année')], null=True, blank=True)
    field = models.CharField(max_length=2, choices=[('1', '2IA'), ('2', 'IDSIT'), ('3', 'IDF'), ('4', 'BI&A'), ('5', 'GL'), ('6', 'GD'), ('7', 'SSI'), ('8', 'SSE')], null=True, blank=True)
    department = models.CharField(max_length=2, choices=[('1', '2IA'), ('2', 'IDSIT'), ('3', 'IDF'), ('4', 'BI&A'), ('5', 'GL'), ('6', 'GD'), ('7', 'SSI'), ('8', 'SSE')], null=True, blank=True)


class PDFUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)  # Add this line
    sujet = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('needs_modification', 'Needs Modification')], default='needs_modification')


    def __str__(self):
        return self.file.name
