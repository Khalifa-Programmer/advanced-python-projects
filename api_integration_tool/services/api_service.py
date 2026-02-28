import requests

def fetch_data():
    url = "https://randomuser.me/api/?results=5"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["results"]
    except requests.exceptions.ConnectionError:
        raise Exception("Network error: Unable to connect to the API.")
    except requests.exceptions.Timeout:
        raise Exception("Network error: API request timed out.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
