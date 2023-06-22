#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import datetime

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


if __name__ == "__main__":
    main()
