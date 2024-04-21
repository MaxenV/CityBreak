import os
from .GUSService import GUSService
from .wordManip import WordManip
from .GoogleService import GoogleService

# Get the GUSkey from environment variables
GUSkey = os.getenv("GUSkey")

# Check if GUSkey is set
if GUSkey is None or GUSkey == "<your_api_key>":
    print(f"GUSkey is not set in environment variables.")
    gusService = GUSService()
else:
    print("GUSkey is set in environment variables.")
    gusService = GUSService(apiKey=GUSkey)

# Check if Google API keys are set
GoogledeveloperKey = os.getenv("GoogledeveloperKey")
GoogleCX = os.getenv("GoogleCX")

if (
    GoogledeveloperKey is None
    or GoogleCX is None
    or GoogledeveloperKey == "<your_api_key>"
    or GoogleCX == "<your_cx>"
):
    print("Google API keys are not set in environment variables.")
    googleService = None
else:
    print("Google API keys are set in environment variables.")
    googleService = GoogleService(GoogledeveloperKey, GoogleCX)

# Create an instance of WordManip
wordManip = WordManip()
