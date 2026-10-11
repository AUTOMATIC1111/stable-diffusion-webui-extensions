from collections import Counter
from pathlib import Path
import datetime
import json


def normalize_git_url(url):
    if not isinstance(url, str):
        raise TypeError(f'URL must be a string: {url!r}')

    normalized = url.strip()
    if not normalized:
        raise ValueError('URL is empty')

    if not normalized.lower().startswith(('http://', 'https://')):
        raise ValueError(f'invalid URL: "{url}"')

    normalized = normalized.rstrip('/')
    if normalized.lower().endswith('.git'):
        normalized = normalized[:-4]

    return normalized


def validate_index(index_path: Path):
    with open(index_path) as inf:
        d = json.load(inf)
        assert "tags" in d

        tags = set(d["tags"].keys())
        seen_urls = set()

        for extension in d["extensions"]:
            for required_key in [
                "name",
                "url",
                "description",
                "added",
                "tags",
            ]:
                assert required_key in extension, f"missing key: {required_key}"

            extension['url'] = normalize_git_url(extension['url'])
            assert extension['url'] not in seen_urls, f'duplicate extension: {extension["url"]}'
            seen_urls.add(extension['url'])

            for tag in extension["tags"]:
                assert tag in tags, f'{extension["url"]} tag: "{str(tag)}" is not a valid tag'

            datetime.date.fromisoformat(extension['added']), "Incorrect data format, should be YYYY-MM-DD"


def validate_entry(file: Path):

    try:
        with open(file, 'r') as f:
            extension = json.load(f)
    except Exception as e:
        exit(f"::error::{file.relative_to(Path().absolute())} : {e}")

    for required_key in [
        "name",
        "url",
        "description",
        "tags",
    ]:
        assert required_key in extension, f"{file} missing key: {required_key}"

    for tag in extension["tags"]:
        assert tag in tags_keys, f'{file} tag: "{str(tag)}" is not a valid tag'

    if extension.get('added'):
        try:
            datetime.date.fromisoformat(extension.get('added'))
        except:
            assert False, f"{file} Incorrect added data format, YYYY-MM-DD"
    normalized_url = normalize_git_url(extension['url'])
    extension['url'] = normalized_url
    return normalized_url


def validate_extension_entrys(ext_dir: Path):
    urls = []
    for f in Path(ext_dir).iterdir():
        if f.is_file() and f.suffix.lower() == '.json':
            urls.append(validate_entry(f))
    counts = Counter(urls)
    duplicates = [element for element, count in counts.items() if count > 1]
    assert len(duplicates) == 0, f'duplicate extension: {duplicates}'
    print(counts)


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent.parent

    with open(base_dir.joinpath('tags.json'), 'r') as f:
        tags_keys = json.load(f).keys()

    validate_extension_entrys(base_dir.joinpath('extensions'))

    validate_index(base_dir.joinpath('index.json'))
