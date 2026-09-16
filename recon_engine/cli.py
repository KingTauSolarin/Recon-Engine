import argparse
import csv
import json
import urllib.request
from pathlib import Path

from recon_engine.scope import ScopeGuard, ScopeError
from recon_engine.ledger import RequestLedger
from recon_engine.models import create_asset


def build_parser():
    parser = argparse.ArgumentParser(
        prog="recon-engine",
        description="UBI Ethical Hacking Stage 5 Recon Engine"
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Target host"
    )

    parser.add_argument(
        "--scope",
        required=True,
        help="Path to scope.csv"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output directory"
    )

    parser.add_argument(
        "--rate",
        type=int,
        default=25,
        help="Maximum requests per second"
    )

    return parser


def main():
    args = build_parser().parse_args()

    output_dir = Path(args.output)
    raw_dir = output_dir / "raw"
    normalized_dir = output_dir / "normalized"

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)

    scope = ScopeGuard(args.scope)
    ledger = RequestLedger(output_dir)

    first_target = None

    with open(args.scope, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row["scope"].upper() == "IN":
                first_target = row
                break

    if first_target is None:
        raise RuntimeError("No authorized IN target found.")

    host, port = first_target["asset"].split(":")
    port = int(port)

    scope.validate(host, port)

    url = f"http://{host}:{port}/"

    with urllib.request.urlopen(url, timeout=5) as response:
        body = response.read().decode("utf-8", errors="replace")

    raw_file = raw_dir / f"{host}_{port}.txt"

    raw_file.write_text(body, encoding="utf-8")

    asset = create_asset(
        target=host,
        port=port,
        protocol="tcp",
        service="http",
        source_tool="urllib",
        source_file=str(raw_file),
        confidence=1.0,
        notes="Initial HTTP discovery"
    )

    normalized_file = normalized_dir / "assets.jsonl"

    with open(normalized_file, "a", encoding="utf-8") as outfile:
        outfile.write(json.dumps(asset.__dict__) + "\n")

    ledger.log(
        host,
        port,
        "tcp",
        "SUCCESS",
        "HTTP discovery completed"
    )

    run_data = {
        "target": args.target,
        "scope": args.scope,
        "output": str(output_dir),
        "rate": args.rate,
        "status": "SUCCESS"
    }

    with open(output_dir / "run.json", "w", encoding="utf-8") as outfile:
        json.dump(run_data, outfile, indent=4)

    print("Recon completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except ScopeError as e:
        print(f"Scope Error: {e}")
    except Exception as e:
        print(f"Error: {e}")