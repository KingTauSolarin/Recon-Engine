import hashlib
import json


def sha256_text(text):

    return hashlib.sha256(
        text.encode()
    ).hexdigest()


def write_json(path, data):

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4
        )