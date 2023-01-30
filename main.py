from flask import Flask, request
import requests

# replace with your actual API keys/access tokens
facebook_access_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
twitter_api_key = "YOUR_TWITTER_API_KEY"
twitter_api_secret = "YOUR_TWITTER_API_SECRET"
linkedin_access_token = "YOUR_LINKEDIN_ACCESS_TOKEN"

app = Flask(_name_)


@app.route("/post", methods=["POST"])
def post():
    message = request.form.get("message")

    # post to Facebook
    facebook_response = requests.post(
        "https://graph.facebook.com/v9.0/me/feed",
        params={"access_token": facebook_access_token},
        json={"message": message}
    )

    # post to Twitter
    # first, get a bearer token for Twitter API
    twitter_bearer_token_response = requests.post(
        "https://api.twitter.com/oauth2/token",
        headers={"Authorization": f"Basic {twitter_api_key}:{twitter_api_secret}"},
        data={"grant_type": "client_credentials"}
    )
    twitter_bearer_token = twitter_bearer_token_response.json()["access_token"]

    twitter_response = requests.post(
        "https://api.twitter.com/1.1/statuses/update.json",
        headers={"Authorization": f"Bearer {twitter_bearer_token}"},
        json={"status": message}
    )

    # post to LinkedIn
    linkedin_response = requests.post(
        "https://api.linkedin.com/v2/shares",
        headers={"Authorization": f"Bearer {linkedin_access_token}"},
        json={
            "author": "urn:li:person:YOUR_LINKEDIN_PROFILE_ID",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": message
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
    )

    return "Post successful!"


if _name_ == "_main_":
    app.run()
