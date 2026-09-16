import json


class Normalizer:

    def write_asset(self, asset, outfile):

        with open(outfile, "a", encoding="utf-8") as f:

            f.write(
                json.dumps(asset.__dict__)
            )

            f.write("\n")