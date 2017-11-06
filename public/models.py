from django.db import models
from django.utils.crypto import get_random_string
from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.urls import reverse


def get_random_32_string():
    return get_random_string(length=32)


class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    discord = models.BooleanField(null=False, default=False)
    avatar = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.user.username + "'s info"

    def get(user):
        try:
            info = UserInfo.objects.get(user=user)
        except:
            info = UserInfo(user=user)
            info.save()
        return info

    def is_discord(user):
        return UserInfo.get(user).discord


class Server(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=True)
    staff = models.BooleanField(null=False, default=False)
    account = models.ForeignKey(User, null=True)

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
    appealWaitHours = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " (" + self.key + ")"


class Log(models.Model):
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

    # Whether this Log is allowed to be appealed or not
    def can_appeal(self):
        return self.progress() < 1 or not self.has_time()

    # Whether it is within the appropriate time to appeal this Log or not
    def should_appeal(self):
        if not self.has_time():
            return True
        else:
            wait = self.punishment.appealWaitHours
            if wait > 0:
                if self.time_elapsed() < wait:
                    return False
            return True

    def has_time(self):
        return self.punishment.timeInHours > 0

    # time elapsed in hours
    def time_elapsed(self):
        diff = datetime.now(timezone.utc) - self.actionTime
        return diff / timedelta(hours=1)

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
        tok = ""
        while True:
            tok = get_random_string(length=32)
            try:
                APIToken.objects.get(token=tok)
            except:
                break

        newToken = APIToken(
            token=tok,
            name=name
        )
        newToken.save()
        return newToken