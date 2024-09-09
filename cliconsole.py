import requests
import json

def send_request(url, method, data):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=json.loads(data))
        elif method == "PUT":
            response = requests.put(url, json=json.loads(data))
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError("Invalid method")

        response_text = f"Status Code: {response.status_code}\n"
        try:
            json_response = response.json()
            formatted_response = json.dumps(json_response, indent=4)
            response_text += f"Response:\n{formatted_response}"
        except json.JSONDecodeError:
            response_text += f"Response:\n{response.text}"
        return response_text
    except requests.RequestException as e:
        return f"Request Error: {e}"

def main():
    print("API Client")
    url = input("Enter the API URL: ")
    method = input("Enter the HTTP method (GET, POST, PUT, DELETE): ")
    data = input("Enter the data to send (JSON format) or leave blank: ") # try this {"key": "value"}
    
    if not data:
        data = "{}"  # Default to empty JSON if no data is provided

    response = send_request(url, method, data)
    print(response)

if __name__ == "__main__":
    main()