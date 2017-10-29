from django.db import models
from datetime import datetime, timezone, timedelta

class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    staff = models.BooleanField(null=False, default=False)

    def display(self):
        if self.name:
            return self.name
        return self.username

    def __str__(self):
        if self.name:
            return self.name + " (" + self.username + ")"
        else:
            return self.username

    def getUser(username):
        try:
            user = User.objects.get(username=username)
        except Exception:
            user = User(username=username)
            user.save()
        return user


class Punishment(models.Model):
    key = models.CharField(max_length=30, primary_key=True)
    name = models.TextField(max_length=100, null=False, blank=False)
    timeInHours = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " (" + self.key + ")"


class Log(models.Model):
    punished = models.ForeignKey(User, related_name="user_punished",null=False)
    reason = models.TextField(max_length=500, null=False)
    punishment = models.ForeignKey(Punishment, null=False)
    staff = models.ForeignKey(User, related_name="staff_punisher", null=False)
    actionTime = models.DateTimeField(auto_now_add=True, primary_key=True)

    def __str__(self):
        return self.staff.display() + " punished " + self.punished.username + " at " + str(self.actionTime)

    def progress(self):
        timeDiff = datetime.now(timezone.utc) - self.actionTime
        progress = timeDiff / timedelta(hours=self.punishment.timeInHours)
        if progress > 1:
            progress = 1
        return progress

    def progress_percent(self):
        return self.progress() * 100

    def progress_percent_rounded(self):
        return int(round(self.progress_percent(), 0))

class APIToken(models.Model):
    token = models.CharField(max_length=50, null=False, primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return 'Token "' + self.name + '"'