from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import re

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
    request = youtube.videos().list(part="statistics", id=video_id)
    response = request.execute()

    if not response["items"]:
        print("No video found.")
        return None

    video = response["items"][0]
    view_count = video["statistics"]["viewCount"]
    return view_count

def get_video_details(youtube, video_id):
    # Get the video details (including title and categoryId)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    if not response["items"]:
        print("No video found.")
        return None, None

    video = response["items"][0]
    title = video["snippet"]["title"]
    category_id = video["snippet"]["categoryId"]
    return title, category_id

def get_valid_categories(youtube):
    # Retrieve valid video categories
    request = youtube.videoCategories().list(part="snippet", regionCode="US")
    response = request.execute()

    categories = {}
    for item in response["items"]:
        categories[item["id"]] = item["snippet"]["title"]
    return categories

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

    # Get the current video title and categoryId
    current_title, category_id = get_video_details(youtube, video_id)

    if current_title is None or category_id is None:
        print("Failed to retrieve video details.")
        return

    # Get the list of valid categories
    valid_categories = get_valid_categories(youtube)

    # Check if the retrieved category_id is valid
    if category_id not in valid_categories:
        print(f"Invalid categoryId: {category_id}. Using a default category.")
        category_id = "22"  # Default category ID (People & Blogs)

    # Debug: Print current title and view count
    print(f"Current Title: {current_title}")
    print(f"View Count: {view_count}")

    # Check if the title already contains a 'View Count' placeholder (or any existing count)
    if "View Count:" in current_title:
        # Replace the view count in the title (use regex to find it)
        new_title = re.sub(r'View Count: \d+', f'View Count: {view_count}', current_title)
    else:
        # Append the view count to the title if no placeholder exists
        new_title = f"{current_title} | View Count: {view_count}"

    # Debug: Print the new title after replacement
    print(f"New Title (after replacement): {new_title}")

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
                "categoryId": category_id,  # Add the valid categoryId here
            },
        },
    )

    # Debug: Print before executing the update request
    print(f"Updating video with Title: {new_title}")

    update_request.execute()
    print(f"Updated title to: {new_title}")

if __name__ == "__main__":
    update_video_title()
