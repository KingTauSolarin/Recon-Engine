import csv
from pathlib import Path
from datetime import datetime


class RequestLedger:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.file = self.output_dir / "request-ledger.csv"

        if not self.file.exists():
            with open(self.file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "target",
                    "port",
                    "protocol",
                    "status",
                    "notes"
                ])

    def log(self, target, port, protocol, status, notes=""):
        with open(self.file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                target,
                port,
                protocol,
                status,
                notes
            ])