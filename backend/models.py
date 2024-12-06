from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ChatGPTAPI import ChatGPTAPI

class Draft(models.Model):
  repositoryLink = models.URLField(max_length=255)
  userDescription = models.TextField()
  postAudience = models.CharField(max_length=50)
  postTone = models.CharField(max_length=50)
  postStyle = models.CharField(max_length=50)
  postHashtags = models.TextField()
  aiPrompt = models.TextField()
  generatedDescription = models.TextField()
  date = models.DateField(auto_now_add=True)
  time = models.TimeField(auto_now_add=True)
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
    self.save()

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

  def setPrompt(self):
    self.aiPrompt = "You will be generating a LinkedIn post by reading this GitHub repository: " + str(self.repositoryLink) + ". Please create the post description for a " + self.postAudience + " audience with a " + self.postTone + " tone and a " + self.postStyle + " style. The following is a description of the GitHub repository, which you will use to understand the purpose and use of the repository provided to you previously: " + self.userDescription + ". Also include these hashtags in the post: " + self.postHashtags + ". Only return the following in your response: a description for a LinkedIn post about the repository provided, a link to the repositories, and the hashtags provided."  

  def getPrompt(self):
    return self.aiPrompt

  def setDescription(self):
    self.setPrompt()
    self.generatedDescription = self.aiAccess.generateDescription(self.getPrompt())
    self.save()
    
  def getDescription(self):
    return self.generatedDescription
  
  def validatePostCompletion(self):
    return bool(self.respositoryLink and (self.generatedDescription or self.userDescription))

  def saveDraft(self, repoLink, userDescription, audience, tone, style, hashtags):
    self.setRepoLink(repoLink)
    self.setUserDescription(userDescription)
    self.setAudience(audience)
    self.setTone(tone)
    self.setStyle(style)
    self.setHastags(hashtags)
    self.setDateAndTime()
    self.setPrompt()
    self.setDescription()
    self.save()

class Post(models.Model):
  description = models.TextField()
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

  def getDrafts(self):
    return self.drafts.all()

  def getPosts(self):
    return self.posts.all()

  def addDraft(self, draft):
    self.drafts.add(draft)

  def addPost(self, post):
    self.posts.add(post)

  def removeDraft(self, draft):
    self.drafts.remove(draft)

