from json import load, loads, dump
from re import compile
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, wait
from urllib.request import Request, urlopen

github_repo_pattern = compile(r'https://github\.com/([^/ ]+/[^/ ]+?)(?:(?:\.git$)|$)')

def get_github_api(url: str):
    try:
        req = Request(url, headers=headers)
        with urlopen(req) as response:
            data = response.read().decode()
            if response.getcode() == 200:
                return True, loads(data)
            else:
                print(f'ERROR {url} Code : {response.getcode()} : {data}')
                return False, None
    except Exception as e:
        print(f"ERROR {url} : {e}")
        return False, None


def get_github_api_limit():
    success, rate_limit = get_github_api('https://api.github.com/rate_limit')
    if success:
        core_limit = rate_limit.get('resources').get('core')
        print(f'core: {core_limit}')
        return(core_limit)
    assert False


def get_github_metadata(extension: dict):
    global get_github_api_call_failed
    # only for github repo
    github_repo = github_repo_pattern.match(extension['url'])
    if github_repo:
        if get_github_api_call_failed:
            print(f"SKIP {extension['url']}")
            return
        print(extension['url'])
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
                else:
                    get_github_api_call_failed = True
        else:
            get_github_api_call_failed = True


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--max-thread", "-m", type=int, default=1, required=False)
    parser.add_argument("--github-token", "-t", type=str, default=None, required=False)
    args = parser.parse_args()

    headers = {'authorization': f'Bearer {args.github_token}'} if args.github_token else {}
    get_github_api_call_failed = False

    with open('index.json', 'r') as f:
        extension_index = load(f)
    
    github_api_core_rait_limit = get_github_api_limit()

    if github_api_core_rait_limit.get('remaining') == 0:
        print('WARNING Rate Limit Exceeded')
        exit()
    elif len(extension_index['extensions'] * 2) >= github_api_core_rait_limit.get('remaining'):
        print('WARNING Rate Limit')

    get_github_api_call_failed = False

    with ThreadPoolExecutor(max_workers=args.max_thread) as executor:
        threads = [executor.submit(get_github_metadata, extension) for extension in extension_index['extensions']]
        wait(threads)

    with open('index.json', 'w') as f:
        dump(extension_index, f, indent=4)
    
    get_github_api_limit()
