import requests
import json
import re
import argparse
from concurrent.futures import ThreadPoolExecutor, wait


def get_github_api(url: str):
    responce = requests.get(url, headers=headers)
    if responce.status_code == 200:
        return True, responce.json()
    else:
        print(f'{url} Code:{responce.status_code} {responce.json()}')
        return False, None
    

def get_github_metadata(extension: dict):
    # only for github repo
    github_repo = github_repo_pattern.match(extension['url'])
    if github_repo:
        success, responce_json = get_github_api(f'https://api.github.com/repos/{github_repo.group(1)}')
        if success:
            extension["full_name"] = responce_json.get("full_name")
            extension["github_description"] = responce_json.get("description")
            extension["stars"] = responce_json.get("stargazers_count")
            extension["default_branch"] = responce_json.get("default_branch")
            extension["created_at"] = responce_json.get("created_at")

            # get metadata of default branch
            if responce_json.get("default_branch"):
                success, responce_json = get_github_api(f'https://api.github.com/repos/{github_repo.group(1)}/branches/{responce_json.get("default_branch")}')
                if success:
                    extension["default_branch_commit_sha"] = responce_json.get("commit").get("sha")
                    extension["commit_time"] = responce_json.get("commit").get("commit").get("author").get("date")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-thread", "-m", type=int, default=1, required=False)
    parser.add_argument("--github-token", "-t", type=str, default=None, required=False)
    args = parser.parse_args()

    headers = {'authorization': f'Bearer {args.github_token}'} if args.github_token else {}
    github_repo_pattern = re.compile(r'https://github\.com/([^/]+/[^/]+?)(?:(?:\.git)|$)')

    with open('index.json', 'r') as f:
        extension_index = json.load(f)

    with ThreadPoolExecutor(max_workers=args.max_thread) as executor:
        threads = [executor.submit(get_github_metadata, extension) for extension in extension_index['extensions']]
        wait(threads)

    with open('index.json', 'w') as f:
        json.dump(extension_index, f, indent=4)
