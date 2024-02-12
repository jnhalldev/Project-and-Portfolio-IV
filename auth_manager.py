import requests

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
        print("Login successful:", response_data)
        return response_data
    else:
        # Handle error
        print("Failed to log in:", response_data.get("error", {}).get("message", "Unknown error"))
        return None

import requests

def register(email, password):
    api_key = "AIzaSyCQmi-nmvKtIE304cvwdqZEJrWy0LZIF4I"  # Replace with your actual Firebase Web API key
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
        return {"success": False, "error": response_data.get("error", {}).get("message", "Unknown error")}

def logout():
    # If you're storing the user's token or any session data, clear it here
    # For this example, we'll just print a message
    print("User logged out")