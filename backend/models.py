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
  aiAccess = ChatGPTAPI()
  
  def setTone(self, tone):
    self.postTone = tone
    self.save()
    
  def setStyle(self, style):
    self.postStyle = style
    self.save()
  
  def setHastags(self, hashtags):
    self.postHashtags = hashtags
    self.save()

  def generateDescription(self):
    # call's chatgpt_api
    # awaiting implementation
    self.save()

  def setDescription(self, description):
    self.generatedDescription = description
    self.save()

  def setUserDescription(self, description):
    self.generatedUserDescription = description
    self.save()

  def setRepoLink(self, link):
    self.respositoryLink = link
    self.save()
    
  def getDescription(self):
    return self.generatedDescription

  def setAudience(self):
    self.postAudience = audience
    seld.save()

  def getDate(self):
    return self.date
    
  def getTime(self):
    return self.time
  
  def validatePostCompletion(self):
    return bool(self.respositoryLink and (self.generatedDescription or self.userDescription))

  def saveDraft(self):
    self.save()

  def setDateAndTime(self, date, time):
    self.date = date
    self.time = time
    self.save()

class Post(models.Model):
  description = models.TextFeild()
  date = models.DateFeild(auto_now_add=True)
  time = models.TimeFeild(auto_now_add=True)

  def fillFromDraft(self, draft):
    self.description = draft.getDescription()
    self.date = datetime.now.date()
    self.time = datetime.now.time()
    self.save()

  def getDescription(self):
    return self.description

  def setDateAndTime(self):
    self.date = datetime.now.date()
    self.time = datetime.now.time()
    self.save()

  def getDate(self):
    return self.date

  def getTime(self):
    return self.time

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  drafts = models.ManyToManyField(Draft, blank=True, related_name="user_profiles")
  posts = models.ManyToManyField(Post, blank=True, related_name="user_profiles")
  linkedInAccess = models.CharField(max_length=255)
  githubAccess = models.CharField(max_length=255)
  username = models.CharField(max_length=150, unique=True)

  def getDrafts(self):
    return self.drafts.all()

  def getPosts(self):
    return self.posts.all()

  def postToLinkedIn(self, post):
    # to be implemented

  def archivePost(self, post):
    self.posts.add(post)

  def refreshLinkedInAccess(self):
    # to be implemented

  def refreshGithubAccess(self):
    # to be implemented

  def addDraft(self, draft):
    self.drafts.add(draft)

  def removeDraft(self, draft):
    self.drafts.remove(draft)

  def authenticateLinkedIn(self):
    # to be implemented

  def authenticateGithub(self):
    # to be implemented

  def getRepositories(self):
    # to be implemented
