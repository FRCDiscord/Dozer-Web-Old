from django.db import models
from django.utils.crypto import get_random_string
from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404


def get_random_32_string():
    return get_random_string(length=32)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord = models.BooleanField(null=False, default=False)
    avatar = models.CharField(max_length=70, null=False, blank=True)

    def __str__(self):
        return self.display() + "'s info"

    def get(user):
        if user:
            try:
                info = UserInfo.objects.get(user=user)
            except:
                info = UserInfo(user=user)
                info.save()
            return info
        else:
            return None

    def is_discord(user):
        return UserInfo.get(user).discord

    def display(self):
        if self.discord:
            return self.user.first_name + "#" + self.user.last_name
        else:
            return self.user.username


class Server(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, null=False, blank=False)
    logo = models.CharField(max_length=80, null=True, default="https://discordapp.com/assets/1c8a54f25d101bdc607cec7228247a9a.svg")

    color = models.CharField(max_length=10, null=True, default="#3f51b5")
    invite = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

    def get(id):
        server = get_object_or_404(Server, id=id)
        return server


class Member(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=True)
    account = models.ForeignKey(User, null=True)
    staff = models.BooleanField(null=False, default=False)
    server = models.ForeignKey(Server, null=False)

    def display(self):
        if self.name:
            return self.name
        return self.username

    def __str__(self):
        if self.name:
            return self.name + " (" + self.username + ")"
        else:
            return self.username

    def getMember(server, username=None, user=None):
        if username is not None:
            try:
                member = Member.objects.get(username=username, server=server)
            except:
                member = Member(username=username, server=server)
                member.save()
            return member
        elif user is not None and UserInfo.get(user).discord:
            try:
                member = Member.objects.get(account=user, server=server)
            except:
                info = UserInfo.get(user)
                member = Member(username=info.display(), account=user, server=server)
                member.save()
            return member
        else:
            return None


class Punishment(models.Model):
    key = models.CharField(max_length=30)
    name = models.TextField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name + " (" + self.key + ")"


class Log(models.Model):
    decision_choices = (
        ("manual", "manual"),
        ("progression", "progression")
    )
    id = models.IntegerField(primary_key=True)
    type_decision = models.CharField(max_length=10, blank=False, choices=decision_choices, default="manual")
    punished = models.ForeignKey(Member, related_name="user_punished",null=False)
    reason = models.TextField(max_length=500, null=False, default="Unknown")
    punishment = models.ForeignKey(Punishment, null=False)
    staff = models.ForeignKey(Member, related_name="staff_punisher", null=False)
    actionTime = models.DateTimeField(auto_now_add=True)
    timeInHours = models.IntegerField(default=0)
    appealWaitHours = models.IntegerField(default=0)
    server = models.ForeignKey(Server, null=False)

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
            wait = self.appealWaitHours
            if wait > 0:
                if self.time_elapsed() < wait:
                    return False
            return True

    def has_time(self):
        return self.timeInHours > 0

    # time elapsed in hours
    def time_elapsed(self):
        diff = datetime.now(timezone.utc) - self.actionTime
        return diff / timedelta(hours=1)

    def progress(self):
        if self.timeInHours > 0:
            timeDiff = datetime.now(timezone.utc) - self.actionTime
            progress = timeDiff / timedelta(hours=self.timeInHours)
            if progress > 1:
                progress = 1
            return progress
        return 1;

    def progress_percent(self):
        return self.progress() * 100

    def progress_percent_rounded(self):
        return int(round(self.progress_percent(), 0))


class Mail(models.Model):
    sender = models.CharField(max_length=50, blank=False)
    subject = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=2000, blank=False)
    server = models.ForeignKey(Server, null=False)

    user = models.ForeignKey(UserInfo, null=True)
    read = models.BooleanField(default=False)

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