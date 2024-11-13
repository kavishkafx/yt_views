import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Scopes needed for YouTube API access
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Replace these with your client ID and client secret from Google Cloud Console
    client_id = ""
    client_secret = ""

    # OAuth flow
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        },
        SCOPES,
    )

    # Use run_local_server instead of run_console
    creds = flow.run_local_server(port=0)
    
    # Save refresh token
    print("Access Token:", creds.token)
    print("Refresh Token:", creds.refresh_token)
    print("Save the refresh token securely; you’ll use it in your GitHub Actions secrets.")

if __name__ == "__main__":
    main()
