import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os, base64, random, json

def generateServiceAccount():
  encodedJson = os.getenv('servacc')
  if encodedJson:
    decodedJson = base64.b64decode(encodedJson)
    decodedDict = json.loads(decodedJson)

    return decodedDict

def generatePass():
  alphanumeric = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  passw = u''

  while len(passw) < 25:
    passw += random.choice(alphanumeric)
  return passw

class DB():
  def __init__(self):
    cred = generateServiceAccount()
    cert = credentials.Certificate(cred)
    self.app = firebase_admin.initialize_app(cert)
    self.firestore = firestore.client()
    self.ids = self.firestore.collection(u'ids')

  def getContent(self, id):
    link = self.ids.document(id)
    if link.get().exists:
      return link
    return False

  def setContent(self, markdown, password, title, color):
    alphanumeric = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    while True:
      uuid = u''
      while len(uuid) < 25:
        uuid += random.choice(alphanumeric)
      for ID in self.ids.stream():
        if uuid == ID.id:
          continue
      break

    newid = self.ids.document(uuid)
    newid.set({
      'md': markdown,
      'pass': password,
      'title': title,
      'color': color
    })

    return uuid
        
  def editContent(self, uuid, markdown, title, color, password):
    editid = self.ids.document(uuid)
    print(editid.get().to_dict())
    editid.update({
      'md': markdown,
      'title': title,
      'color': color,
      'pass': password,
    })


