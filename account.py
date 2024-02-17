userIDToken = ""
userID = ""
dabaseURL = 'https://resu-hunter-default-rtdb.firebaseio.com/'

def GetUserIDToken():
    return userIDToken

def SaveUserIDToken(idToken):
    global userIDToken
    userIDToken = idToken

def ClearUserIDToken():
    global userIDToken
    userIDToken = ""

def GetUserID():
    return userID

def SaveUserID(id):
    global userID
    userID = id

def ClearUserID():
    global userID
    userID = ""

def GetDatabaseURL():
    return dabaseURL