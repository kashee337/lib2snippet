import glob
import json
import os
import sys
from collections import OrderedDict

import yaml


def packing_codebody(filepath):
    with open(filepath, "r") as f:
        code_strlist = [line.strip() for line in f.readlines()]
    return code_strlist


def gen_filedict(filepath):
    prefix = os.path.splitext(os.path.basename(filepath))[0]
    body = packing_codebody(filepath)
    dic = OrderedDict()
    dic["prefix"] = prefix
    dic["body"] = body
    return dic


def is_overwrite(output_path):
    if not os.path.isfile(output_path):
        return True
    key = None
    while key not in ["y", "n"]:
        key = input("{} is exist : overwrite? y/n\n".format(output_path))
    return key == "y"


if __name__ == "__main__":
    assert len(sys.argv) > 1, "please set the path to config.yaml"
    cfg_path = sys.argv[1]
    assert os.path.isfile(cfg_path), "{} is not exist".format(cfg_path)

    with open(cfg_path, "rb") as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    for lang, input_dir in cfg["lib_dir"].items():
        try:
            os.makedirs(cfg["output"], exist_ok=True)
            output_path = os.path.join(cfg["output"], "{}.json".format(lang))
            input_path = os.path.join(input_dir, "*.{}".format(lang))
            # overwrite check
            if not cfg["overwrite"]:
                if not is_overwrite(output_path):
                    continue
            # make code-snippets json
            filelist = sorted(glob.glob(input_path))
            snippets_dict = dict()
            for filepath in filelist:
                file_dict = gen_filedict(filepath)
                name = file_dict["prefix"]
                snippets_dict[name] = file_dict
            # save
            with open(output_path, "w") as f:
                json.dump(snippets_dict, f, indent=4)
                print("{} : save".format(output_path))
        except TypeError:
            print("{} : invalid format".format(lang))
