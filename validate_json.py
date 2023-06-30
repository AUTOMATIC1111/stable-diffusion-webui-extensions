#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import datetime
from re import compile
from collections import Counter

git_url_pattern = compile(r'(https://[^ ]+?)(?:(?:\.git)$|$)')

def operation(
    *,
    path_in: Path,
    path_out: Path,
) -> None:
    with path_in.open() as inf, path_out.open("w") as outf:
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

            for _tag in extension["tags"]:
                assert _tag in tags

            datetime.date.fromisoformat(extension['added']), "Incorrect data format, should be YYYY-MM-DD"


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument(
        "--input", "-i", type=Path, default="/dev/stdin", required=False
    )
    oparser.add_argument(
        "--output", "-o", type=Path, default="/dev/stdout", required=False
    )
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
    )


with open('tags.json', 'r') as f:
    tags = json.load(f)

tags_keys = tags.keys()

def validate_extension_entry(file: Path):

    with open(file, 'r') as f:
        extension = json.load(f)
    for required_key in [
        "name",
        "url",
        "description",
        "tags",
    ]:
        assert required_key in extension, f"{file} missing key: {required_key}"

    for _tag in extension["tags"]:
        assert _tag in tags, f'{file} tag: "{str(_tag)}" is not a valid tag'

    if extension.get('added'):
        try:
            datetime.date.fromisoformat(extension.get('added'))
        except:
            assert False, f"{file} Incorrect added data format, YYYY-MM-DD"
    git_url = git_url_pattern.match(extension['url'])
    assert git_url, f'invalid URL: "{extension["url"]}"'
    return git_url.group(1)


def duplicate_test(lst: list):
    counts = Counter(lst)
    duplicates = [element for element, count in counts.items() if count > 1]
    assert len(duplicates) == 0, f'duplicate extension: {duplicates}'
    return duplicates


if __name__ == "__main__":
    urls = []
    for f in Path('extensions').iterdir():
        if f.is_file() and f.suffix.lower() == '.json':        
            urls.append(validate_extension_entry(f))
    duplicate_test(urls)
    main()
