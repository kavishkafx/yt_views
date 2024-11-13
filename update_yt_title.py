import os
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_authenticated_service():
    # Authenticate using the OAuth credentials and refresh token
    creds = Credentials.from_authorized_user_info(
        {
            "client_id": os.environ["YT_CLIENT_ID"],
            "client_secret": os.environ["YT_CLIENT_SECRET"],
            "refresh_token": os.environ["YT_REFRESH_TOKEN"],
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    )
    return build("youtube", "v3", credentials=creds)

def get_view_count(youtube, video_id):
    # Get the video statistics
    try:
        request = youtube.videos().list(part="statistics", id=video_id)
        response = request.execute()

        if not response["items"]:
            print("No video found.")
            return None

        video = response["items"][0]
        view_count = video["statistics"]["viewCount"]
        return view_count
    except Exception as e:
        print(f"Error retrieving view count: {e}")
        return None

def get_video_details(youtube, video_id):
    # Get the video details (including title and categoryId)
    try:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()

        if not response["items"]:
            print("No video found.")
            return None, None

        video = response["items"][0]
        title = video["snippet"]["title"]
        category_id = video["snippet"]["categoryId"]
        return title, category_id
    except Exception as e:
        print(f"Error retrieving video details: {e}")
        return None, None

def get_valid_categories(youtube):
    # Retrieve valid video categories
    try:
        request = youtube.videoCategories().list(part="snippet", regionCode="US")
        response = request.execute()

        categories = {}
        for item in response["items"]:
            categories[item["id"]] = item["snippet"]["title"]
        return categories
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        return {}

def update_video_title():
    # Authenticate and get the YouTube service
    youtube = get_authenticated_service()

    # Get the video ID from the environment variable
    video_id = os.environ["YT_VIDEO_ID"]

    # Get the current view count of the video
    view_count = get_view_count(youtube, video_id)

    if view_count is None:
        print("Failed to retrieve view count.")
        return

    # Format the view count with commas
    view_count = f"{int(view_count):,}"

    # Get the current video title and categoryId
    _, category_id = get_video_details(youtube, video_id)

    if category_id is None:
        print("Failed to retrieve video details.")
        return

    # Get the list of valid categories
    valid_categories = get_valid_categories(youtube)

    # Check if the retrieved category_id is valid
    if category_id not in valid_categories:
        print(f"Warning: Invalid categoryId '{category_id}' retrieved. Falling back to default category.")
        category_id = "22"  # Default category ID (People & Blogs)

    # Construct the new title based on the specified format
    new_title = f"Real-Time? Not Quite... Views: {view_count} (Updated Every 10 Minutes to Spare the API!)"

    # Ensure the title is within YouTube's title length limit (100 characters)
    new_title = new_title[:100]

    # Validate that the title is not empty
    if not new_title.strip():
        print("Error: The new title is empty or invalid.")
        return

    # Update the video title along with the categoryId
    update_request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": new_title,
                "categoryId": category_id,
            },
        },
    )

    # Debug: Print before executing the update request
    print(f"Updating video with Title: {new_title}")

    # Try executing the update request
    try:
        update_request.execute()
        print(f"Updated title to: {new_title}")
    except Exception as e:
        print(f"Failed to update title: {e}")

if __name__ == "__main__":
    update_video_title()
