import json


def load_json(json_path):
    # print("yes")
    with open(json_path, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip() != ""]


def save_normal_json(json_info, json_path):
    with open(json_path, "w") as f:
        for info in json_info:
            print(json.dumps(info, ensure_ascii=False), file=f)
