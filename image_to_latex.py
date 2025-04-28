import requests

# URL of the FastAPI server
url = "http://127.0.0.1:8502/predict/"

# Path to your image file
image_path = "iamge.png"  # Replace with the path to your image file

# Open the image file in binary mode
with open(image_path, 'rb') as img_file:
    # Prepare the files to be sent in the request
    files = {'file': img_file}
    # Send POST request to the API
    response = requests.post(url, files=files)

# Check if the request was successful
if response.ok:
    # Print the LaTeX code returned by the API
    latex_code = response.json()
    print("LaTeX Code:", latex_code)
else:
    print("Error:", response.text)
