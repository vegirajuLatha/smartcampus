# from django.db import models

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# class Announcement(models.Model):
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     created_at = models.DateTimeField(default=timezone.now)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

# class AnnouncementRead(models.Model):
#     announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     read_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('announcement', 'student')
