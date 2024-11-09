import models
class ChatGPTAPI():
  str apiKey
  str endpoint

  def authentice():
    if apiKey and endpoint:
      return True
    else:
      return False

  def generateDescription(draft):
    return draft.getUserDescription()
  
