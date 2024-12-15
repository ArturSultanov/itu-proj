import requests

BASE_URL = "http://localhost:8000"  # Update this based on your FastAPI server

def api_request(route: str, params: dict = None, method: str = "GET"):
    """
    Helper function to make API calls to FastAPI backend.
    
    :param route: The API route (e.g., '/login' or '/current_player').
    :param params: Parameters to be passed in the request (e.g., username and password).
    :return: Response from the API.
    """
    try:
        url = f"{BASE_URL}{route}"
        if method == "POST":
            response = requests.post(url, json=params)
        elif method == "GET":
            response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {"message": "Error: " + response.text}
    except Exception as e:
        return {"message": f"Request failed: {str(e)}"}