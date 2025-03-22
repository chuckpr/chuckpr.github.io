import pathlib
import nbformat
import re
import yaml


def parse_raw_metadata(s):
    match = re.search(r"---\n(.*?)\n---", s, re.DOTALL)
    if match:
        metadata_str = match.group(1)
        metadata = yaml.safe_load(metadata_str)
        return metadata
    else:
        return {}


def get_metadata(post_p):
    if post_p.suffix == ".ipynb":
        nb = nbformat.read(post_p, as_version=4)
        metadata_raw = nb["cells"][0]["source"]
    elif post_p.suffix == ".qmd":
        with open(post_p, "r") as fh:
            metadata_raw = fh.read()
    else:
        metadata_raw = ""
    data = parse_raw_metadata(metadata_raw)
    data["path"] = str(post_p)
    data["type"] = str(post_p.parents[-2])
    return data


if __name__ == "__main__":
    files = []
    exts = [".ipynb", ".qmd"]
    paths = ["til", "posts"]
    for ext, path in zip(exts, paths):
        files.extend(pathlib.Path(f"{path}/").glob(f"**/*{ext}"))
    yaml_str = yaml.dump([get_metadata(p) for p in files])
    with open("listing.yaml", "w") as fh:
        fh.write(yaml_str)
