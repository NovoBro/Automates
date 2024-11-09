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

  def setRepoLink(self, link):
    self.respositoryLink = link
    self.save()

  def getRepoLink(self):
    return self.repositoryLink

  def setUserDescription(self, description):
    self.generatedUserDescription = description
    self.save()
    
  def getUserDescription(self):
    return self.userDescription

  def setAudience(self, audience):
    self.postAudience = audience
    seld.save()

  def getAudience(self):
    return self.postAudience
  
  def setTone(self, tone):
    self.postTone = tone
    self.save()

  def getTone(self):
    return self.tone
    
  def setStyle(self, style):
    self.postStyle = style
    self.save()

  def getStyle(self):
    return self.style
  
  def setHastags(self, hashtags):
    self.postHashtags = hashtags
    self.save()

  def getHastags(self):
    return self.postHashtags

  def setDateAndTime(self):
    self.date = datetime.now.date()
    self.time = datetime.now.time()
    self.save()

  def getDate(self):
    return self.date
    
  def getTime(self):
    return self.time

  def setDescription(self):
    if aiAccess.authentice():
      self.generatedDescription = aiAccess.generateDescription(self)
    else:
      self.generatedDescription = "AI Authentication Failed."
    self.save()
    
  def getDescription(self):
    return self.generatedDescription
  
  def validatePostCompletion(self):
    return bool(self.respositoryLink and (self.generatedDescription or self.userDescription))

  def saveDraft(self):
    self.save()

class Post(models.Model):
  description = models.TextFeild()
  date = models.DateField(auto_now_add=True)
  time = models.TimeField(auto_now_add=True)

  def fillFromDraft(self, draft):
    self.description = draft.getDescription()
    self.date = datetime.now.date()
    self.time = datetime.now.time()
    self.save()

  def getDescription(self):
    return self.description

  def getDate(self):
    return self.date

  def getTime(self):
    return self.time

  def setDateAndTime(self):
    self.date = datetime.now.date()
    self.time = datetime.now.time()
    self.save()


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  drafts = models.OneToManyField(Draft, blank=True, related_name="user_profiles")
  posts = models.OneToManyField(Post, blank=True, related_name="user_profiles")
  linkedInAccess = models.CharField(max_length=255)
  githubAccess = models.CharField(max_length=255)
  username = models.CharField(max_length=150, unique=True)
  linkedInAccess = LinkedInAPI()
  gitHubAccess = GitHubAPI()

  def authenticateLinkedIn(self):
    # to be implemented

  def authenticateGithub(self):
    # to be implemented

  def refreshLinkedInAccess(self):
    # to be implemented

  def refreshGithubAccess(self):
    # to be implemented

  def getDrafts(self):
    return self.drafts.all()

  def getPosts(self):
    return self.posts.all()

  def getRepositories(self):
    # to be implemented

  def addDraft(self, draft):
    self.drafts.add(draft)

  def addPost(self, post):
    self.posts.add(post)

  def removeDraft(self, draft):
    self.drafts.remove(draft)

  def postToLinkedIn(self, draft):
    post = Post()
    post.fillFromDraft(draft)
    if linkedInAccess.postToLinkedIn(post):
      self.addPost(post)
      self.removeDraft(draft)
      self.save()
      return True
    else:
      return False
