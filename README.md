# YouTube Title Auto-Updater

A recreation of Tom Scott's real-time view counter implementation. Due to YouTube's API quota limitations (and me not wanting to pay Google for additional quota xd), this version updates every 7 minutes. So the view counts might be running a few minutes behind real-time, but hey, it's still pretty cool!

## Video Tutorial
For a detailed walkthrough of setting up a similar system locally, check out [this helpful tutorial](https://www.youtube.com/watch?v=QuUKE4cw4Y8).

## Setup Instructions

### Step 1: Set Up Google Cloud Project and OAuth Credentials

1. Navigate to the [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3** for your project
4. Go to **APIs & Services > Credentials**
5. Create OAuth client credentials:
   - Select **Desktop App** as the application type
   - Note down the generated `client_id` and `client_secret`

### Step 2: Generate a Refresh Token Locally

You'll need to generate a `refresh_token` using your OAuth credentials. This is a one-time process:
- Generate the token locally using the OAuth credentials
- Once obtained, you won't need to store it locally
- The `refresh_token` will be securely stored in GitHub Secrets

### Step 3: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Navigate to **Settings > Secrets and variables > Actions**
3. Add the following repository secrets:

| Secret Name | Description |
|------------|-------------|
| `YT_CLIENT_ID` | Your YouTube API client ID |
| `YT_CLIENT_SECRET` | Your YouTube API client secret |
| `YT_REFRESH_TOKEN` | The refresh token from Step 2 |
| `YT_VIDEO_ID` | The ID of your YouTube video |

## How It Works

The system uses a GitHub Action (`.github/workflows/update_youtube_title.yml`) that:
- Runs automatically every 7 minutes
- Fetches the current view count for your specified video
- Updates the video title with the latest view count
- Provides viewers with an approximately real-time view counter

## Technical Details

- **Update Frequency**: Every 7 minutes (configured to respect YouTube API's daily quota limit of 10,000 units - each title update consumes 50 units. While this aggressive update frequency will consume more API quota, it provides more frequent updates for better accuracy)
- **API Used**: YouTube Data API v3
- **Automation**: GitHub Actions
- **Runtime**: Serverless (no local execution needed after setup)

## Important Notes

- ⚠️ The system runs entirely through GitHub Actions - no local server needed
- 📊 7-minute update interval provides more frequent updates but consumes more API quota
- 🔒 All sensitive credentials are stored securely in GitHub Secrets
- 📝 Remember to keep your API credentials private and never commit them to the repository
- ⏰ View counts may be slightly delayed due to the update interval and API limitations

## Troubleshooting

If you encounter issues:
1. Verify all secrets are correctly set in GitHub
2. Check GitHub Actions logs for any error messages
3. Ensure your Google Cloud Project has the YouTube Data API enabled
4. Confirm your OAuth credentials have the correct scope and permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
