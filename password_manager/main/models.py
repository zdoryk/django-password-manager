from django.db import models


class PasswordEntry(models.Model):
    def __str__(self):
        return f'{self.service} | {self.login}'

    service = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)


# class ChangeLog(models.Model):
#     def __str__(self):
#         return f'{self.model_name} | {self.record_id} | {self.action}'
#
#     model_name = models.CharField(max_length=100)
#     record_id = models.CharField(max_length=100)
#     action = models.CharField(max_length=100)
#     timestamp = models.DateTimeField()
#
#
# class OfflineChangeLog(models.Model):
#     def __str__(self):
#         return f'{self.model_name} | {self.record_id} | {self.action}'
#
#     model_name = models.CharField(max_length=100)
#     record_id = models.CharField(max_length=100)
#     action = models.CharField(max_length=100)
#     timestamp = models.DateTimeField()


class SyncTimestamp(models.Model):
    last_sync = models.DateTimeField()
