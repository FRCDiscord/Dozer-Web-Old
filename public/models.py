from django.db import models
from django.utils.crypto import get_random_string
from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.urls import reverse

def get_random_32_string():
    return get_random_string(length=32)

class Member(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    staff = models.BooleanField(null=False, default=False)
    account = models.ForeignKey(User, null=True)
    verified = models.BooleanField(default=False)

    def display(self):
        if self.name:
            return self.name
        return self.username

    def __str__(self):
        if self.name:
            return self.name + " (" + self.username + ")"
        else:
            return self.username

    def getMember(username):
        try:
            member = Member.objects.get(username=username)
        except:
            member = Member(username=username)
            member.save()
        return member


class Punishment(models.Model):
    key = models.CharField(max_length=30, primary_key=True)
    name = models.TextField(max_length=100, null=False, blank=False)
    timeInHours = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " (" + self.key + ")"


class Log(models.Model):
    key = models.CharField(primary_key=True, max_length=32, default=get_random_32_string)
    punished = models.ForeignKey(Member, related_name="user_punished",null=False)
    reason = models.TextField(max_length=500, null=False, default="Unknown")
    punishment = models.ForeignKey(Punishment, null=False)
    staff = models.ForeignKey(Member, related_name="staff_punisher", null=False)
    actionTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff.display() + " punished " + self.punished.username + " at " + str(self.actionTime)

    def appeal_subject(self):
        return self.staff.display() + "'s " + self.punishment.name + " on me at " + str(self.actionTime)

    def appeal_url(self):
        return reverse('public:mail') + "?appeal=" + self.key

    def has_time(self):
        return self.punishment.timeInHours > 0

    def progress(self):
        if self.punishment.timeInHours > 0:
            timeDiff = datetime.now(timezone.utc) - self.actionTime
            progress = timeDiff / timedelta(hours=self.punishment.timeInHours)
            if progress > 1:
                progress = 1
            return progress
        return 1;

    def progress_percent(self):
        return self.progress() * 100

    def progress_percent_rounded(self):
        return int(round(self.progress_percent(), 0))

class APIToken(models.Model):
    token = models.CharField(max_length=50, null=False, primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=True)
    uses = models.IntegerField(null=False, default=0)

    def __str__(self):
        return 'Token "' + self.name + '"'

    def generateToken(name):
        newToken = APIToken(
            token=get_random_string(length=32),
            name=name
        )
        newToken.save()
        return newToken

