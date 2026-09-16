from dataclasses import dataclass
from datetime import datetime


@dataclass
class Asset:
    observed_at: str
    target: str
    port: int
    protocol: str
    service: str
    source_tool: str
    source_file: str
    confidence: float = 1.0
    notes: str = ""


def create_asset(
    target,
    port,
    protocol,
    service,
    source_tool,
    source_file,
    confidence=1.0,
    notes=""
):
    return Asset(
        observed_at=datetime.utcnow().isoformat(),
        target=target,
        port=port,
        protocol=protocol,
        service=service,
        source_tool=source_tool,
        source_file=source_file,
        confidence=confidence,
        notes=notes,
    )