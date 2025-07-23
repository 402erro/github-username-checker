import requests
import json
import sys

with open('config.json', 'r') as file:
    config = json.load(file)
    PAT = config.get("PAT") 

with open('usernames.txt', 'r') as file:
    usernames = file.readline().strip().split(',')

    for i in usernames:
        username = i

        headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {PAT}',
        'X-GitHub-Api-Version': '2022-11-28',
        }
        response = requests.get(f'https://api.github.com/users/{username}', headers=headers)

        RateRemaining = response.headers.get('x-ratelimit-remaining')
        RateReset = response.headers.get('x-ratelimit-reset')
        RateUsed = response.headers.get('x-ratelimit-used')
        RateLimit = response.headers.get('x-ratelimit-limit')
        TimeTillReset = response.headers.get('x-ratelimit-reset')

        if RateUsed < RateLimit:
            if response.status_code == 200:
                print(f"User: {username} - Status: ❌")
                print(f"Rate Remaining: {RateRemaining}\\{RateLimit}")
            elif response.status_code == 404:
                print(f"User: {username} - Status: ✅")
            elif response.status_code == 403:
                print("Rate limit exceeded or access forbidden.")
                sys.exit(1)

