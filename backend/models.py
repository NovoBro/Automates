from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Draft(models.Model):
  repositoryLink = models.URLFeild(max_length=255)
  userDescription = models.TextFeild()
  postAudience = models.CharField(max_length=50)
  postTone = models.CharField(max_length=50)
  postStyle = models.CharField(max_length=50)
  postHashtags = models.TextFeild()
  generatedDescription = models.TextFeild()
  date = models.DateFeild(auto_now_add=True)
  time = models.TimeFeild(auto_now_add=True)
  
  def setTone(self, tone):

  def setStyle(self, style):

  def setHastags(self, style):

  def generateDescription(self):

  def changeDescription(self, description):

  def changeUserDescription(self, description):

  def setRepoLink(self, link):

  def getDescription(self):

  def setAudience(self):

  def getDate(self):

  def getTime(self):

  def validatePostCompletion(self):

  def saveDraft(self):

  def setDateAndTime(self):
    

class Post(models.Model):
  description = models.TextFeild()
  date = models.DateFeild(auto_now_add=True)
  time = models.TimeFeild(auto_now_add=True)

  def fillFromDraft(self, draft):

  def getDescription(self):

  def setDateAndTime(self):

  def getDate(self):

  def getTime(self):

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  drafts = models.ManyToManyField(Draft, blank=True, related_name="user_profiles")
  posts = models.ManyToManyField(Post, blank=True, related_name="user_profiles")
  linkedInAccess = models.CharField(max_length=255)
  githubAccess = models.CharField(max_length=255)
  username = models.CharField(max_length=150, unique=True)

  def getDrafts(self):

  def getPosts(self):

  def postToLinkedIn(self, post):

  def archivePost(self, post):

  def refreshLinkedInAccess(self):

  def refreshGithubAccess(self):

  def addDraft(self, draft):

  def removeDraft(self, draft):

  def postHistory(self):

  def authenticateLinkedIn(self):

  def authenticateGithub(self):

  def getRepositories(self):
