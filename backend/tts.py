import requests
import boto3
import dotenv

# Obtain environment variables
env_vars = dotenv.dotenv_values()
URL = "https://api.play.ht/api/v2/tts/stream"
X_USER_ID = env_vars['X_USER_ID']
X_AUTH = env_vars['X_AUTH']
X_VOICE = env_vars['X_VOICE']
S3_BUCKET_NAME = env_vars['S3_BUCKET_NAME']
S3_ACCESS_KEY = env_vars['S3_ACCESS_KEY']
S3_SECRET_KEY = env_vars['S3_SECRET_KEY']

# Set up S3 client with credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

# Headers for the API request
headers = {
    "X-USER-ID": X_USER_ID, 
    "AUTHORIZATION": X_AUTH, 
    "accept": "audio/mpeg", 
    "content-type": "application/json"
}

def generate_tts(prompt: str) -> str:
    data = {
        "text": prompt,
        "voice_engine": "PlayHT2.0",
        "voice": X_VOICE,
        "output_format": "mp3"
    }
 
    # Make the POST request
    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        # Save the MP3 content to an S3 bucket
        file_name = "output.mp3"
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=response.content,
            ContentType='audio/mpeg',
            # ACL='public-read'  # Make it publicly accessible
        )

        # Generate public URL
        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        print(f"MP3 file uploaded to S3 and accessible at: {file_url}")
        return file_url
    else:
        print(f"Request failed: {response.status_code}")
        print(response.text)

# Example usage
file_url = generate_tts("I am the second greatest player of all time behind my glorious king Michael Jordan.")
print(f"Access your MP3 at: {file_url}")



