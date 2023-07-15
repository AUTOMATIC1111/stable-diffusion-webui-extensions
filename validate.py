from collections import Counter
from pathlib import Path
import datetime
import json
import re

git_url_pattern = re.compile(r'(https://[^ ]+?)(?:(?:\.git)$|$)')


def validate_index(index_path: Path):
    with open(index_path) as inf:
        d = json.load(inf)
        assert "tags" in d

        tags = set(d["tags"].keys())

        for extension in d["extensions"]:
            for required_key in [
                "name",
                "url",
                "description",
                "added",
                "tags",
            ]:
                assert required_key in extension, f"missing key: {required_key}"

            for tag in extension["tags"]:
                assert tag in tags, f'{extension["url"]} tag: "{str(tag)}" is not a valid tag'

            datetime.date.fromisoformat(extension['added']), "Incorrect data format, should be YYYY-MM-DD"


def validate_entry(file: Path):

    with open(file, 'r') as f:
        extension = json.load(f)
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
    git_url = git_url_pattern.match(extension['url'])
    assert git_url, f'invalid URL: "{extension["url"]}"'
    return git_url.group(1)


def validate_extension_entrys(ext_dir: Path):
    urls = []
    for f in Path(ext_dir).iterdir():
        if f.is_file() and f.suffix.lower() == '.json':
            urls.append(validate_entry(f))
    counts = Counter(urls)
    duplicates = [element for element, count in counts.items() if count > 1]
    assert len(duplicates) == 0, f'duplicate extension: {duplicates}'


if __name__ == "__main__":
    with open(Path('tags.json'), 'r') as f:
        tags_keys = json.load(f).keys()

    validate_extension_entrys(Path('extensions'))

    validate_index(Path('index.json'))
