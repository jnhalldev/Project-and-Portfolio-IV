import requests
from collections.abc import MutableMapping

def login(email, password):
    api_key = "AIzaSyCQmi-nmvKtIE304cvwdqZEJrWy0LZIF4I"
    request_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    
    response = requests.post(request_url, json=data)
    response_data = response.json()

    if response.status_code == 200:
        return {"success": True, "idToken": response_data['idToken'],"localId": response_data['localId']}
    else:
        # Handle error
        errorMessage = response_data.get("error", {}).get("message", "Unknown error")
        print("Failed to log in:", errorMessage)
        return {"success": False, "message": errorMessage}

import requests

def register(email, password):
    api_key = "AIzaSyCQmi-nmvKtIE304cvwdqZEJrWy0LZIF4I" 
    request_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    
    response = requests.post(request_url, json=data)
    response_data = response.json()

    if response.status_code == 200:
        # Registration successful
        return {"success": True, "data": response_data}
    else:
        # Registration failed
        errorMessage = response_data.get("error", {}).get("message", "Unknown error")
        print("Failed to register:", errorMessage)
        return {"success": False, "message": errorMessage}

def logout():
    print("User logged out")