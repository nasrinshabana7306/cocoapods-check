# auto_post.py
# Posts your latest commit as an Instagram update to @naz_ri_h
import os
import time
import requests

IG_USER_ID = os.environ["IG_USER_ID"]
IG_TOKEN = os.environ["IG_ACCESS_TOKEN"]
IMAGE_URL = os.environ.get("IMAGE_URL", "https://your-site.com/cover.jpg")
GH_TOKEN = os.environ["GH_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]

# 1. Get latest commit from GitHub
headers = {"Authorization": f"Bearer {GH_TOKEN}"}
commit_res = requests.get(
    f"https://api.github.com/repos/{REPO}/commits?per_page=1",
    headers=headers,
    timeout=20,
)
commit_res.raise_for_status()
commits = commit_res.json()
if not commits:
    raise RuntimeError("No commits found for repository")
commit = commits[0]
message = commit["commit"]["message"].split("\n")[0]
author = commit["commit"]["author"]["name"]
commit_url = commit["html_url"]
sha_short = commit["sha"][:7]

print(f"Latest commit: {message} by {author}")

# 2. Build caption from commit
CAPTION = f"""Project Update

{message}

Repo: {REPO}
By: {author}
{commit_url}

Auto-posted from GitHub after tests passed
#coding #github #projectupdate #naz_ri_h
"""

# 3. Post to Instagram
BASE = "https://graph.facebook.com/v21.0"

print("Creating Instagram media...")
res = requests.post(
    f"{BASE}/{IG_USER_ID}/media",
    data={
        "image_url": IMAGE_URL,
        "caption": CAPTION,
        "access_token": IG_TOKEN,
    },
    timeout=30,
)
res.raise_for_status()
media = res.json()
print(media)
container_id = media["id"]

time.sleep(10)

print("Publishing...")
publish = requests.post(
    f"{BASE}/{IG_USER_ID}/media_publish",
    data={
        "creation_id": container_id,
        "access_token": IG_TOKEN,
    },
    timeout=30,
)
publish.raise_for_status()
print(publish.json())
print(f"Posted commit {sha_short} to @naz_ri_h!")
