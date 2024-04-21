import os
from .GUSService import GUSService
from .wordManip import WordManip

# Get the GUSkey from environment variables
GUSkey = os.getenv("GUSkey")

# Check if GUSkey is set
if GUSkey is None or GUSkey == "<your_api_key>":
    print(f"GUSkey is not set in environment variables.")
    gusService = GUSService()
else:
    print("GUSkey is set in environment variables.")
    gusService = GUSService(apiKey=GUSkey)


# Create an instance of WordManip
wordManip = WordManip()
