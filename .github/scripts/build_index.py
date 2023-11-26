from argparse import ArgumentParser
from pathlib import Path
import datetime
import json

import validate

def read_extension(file: Path):
    with open(file, 'r', encoding='utf-8') as f:
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

    try:
        datetime.date.fromisoformat(extension.get('added'))
    except:
        # add "added": "YYYY-MM-DD"
        extension["added"] = str(datetime.datetime.now().date())
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(extension, f, indent=4, ensure_ascii=False)
    return extension


def read_extension_dir():
    extensions = {}
    for f in extensions_dir.iterdir():
        if f.is_file() and f.suffix.lower() == '.json':        
            extension = read_extension(f)
            extensions[extension['url']] = extension
    return extensions


def update_index(exts: dict, tags: dict):
    # update existing remove removed and add new extensions
    with open(build_index_path, 'r', encoding='utf-8') as f:
        existing_extensions = {extension['url']: extension for extension in json.load(f)['extensions']}

    for extensions_url, extension in exts.items():
        if extensions_url in existing_extensions.keys():
            existing_extensions[extensions_url].update(extension)
        else:
            existing_extensions[extensions_url] = extension
    extensions_list = [extension for extensions_url, extension in existing_extensions.items() if extensions_url in extensions]
    extension_index = {'tags': tags, 'extensions': extensions_list}

    with open(build_index_path, 'w', encoding='utf-8') as f:
        json.dump(extension_index, f, indent=4, ensure_ascii=False)
    return extension_index


def update_master_index(index: dict):
    # add keys from master/index that are not in extensions/tags to extensions/tags as new master/index
    with open(deploy_index_path, 'r', encoding='utf-8') as f:
        master_exts = {extension['url']: extension for extension in json.load(f)['extensions']}

    index_ext = {extension['url']: extension for extension in index['extensions']}
    index_ext_urls = index_ext.keys()
    for master_ext_url, master_ext in master_exts.items():
        if master_ext_url in index_ext_urls:
            index_ext_keys = index_ext[master_ext_url].keys()
            for master_exts_key in master_ext.keys():
                if master_exts_key not in index_ext_keys:
                    index_ext[master_ext_url][master_exts_key] = master_ext[master_exts_key]

    new_master_index = {'tags': index['tags'], 'extensions': list(index_ext.values())}
    with open(deploy_index_path, 'w', encoding='utf-8') as f:
        json.dump(new_master_index, f, indent=4, ensure_ascii=False)
    return new_master_index


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--build-branch", "-b", type=str, default='', required=False)
    parser.add_argument("--deploy-branch", "-d", type=str, default='', required=False)
    args = parser.parse_args()
    
    build_index_path = Path(args.build_branch).joinpath('index.json')
    deploy_index_path = Path(args.deploy_branch).joinpath('index.json')
    extensions_dir = Path(args.build_branch).joinpath('extensions')

    # read tags
    with open(Path(args.build_branch).joinpath('tags.json'), 'r') as f:
        tags = json.load(f)

    # read entries
    extensions = read_extension_dir()

    # update indexs
    extension_index_ext = update_index(extensions, tags)
    extension_index_master = update_master_index(extension_index_ext)
    
    # validate
    validate.validate_index(build_index_path)
    validate.validate_index(deploy_index_path)

    assert len(extension_index_ext["extensions"]) == len(extension_index_master["extensions"]), f'entry count mismatch: {len(extension_index_ext["extensions"])} {len(extension_index_master["extensions"])}'
    print(f'::notice::{len(tags)} tags, {len(extension_index_ext["extensions"])} extensions')    
