import json
import xml.etree.ElementTree as ET


class ParserError(Exception):
    pass


def parse_nmap_xml(xml_text):
    try:
        root = ET.fromstring(xml_text)

        address = root.find(".//address")
        port = root.find(".//port")
        state = root.find(".//state")
        service = root.find(".//service")

        return {
            "host": address.attrib["addr"],
            "port": int(port.attrib["portid"]),
            "transport": port.attrib["protocol"],
            "service": service.attrib["name"],
            "state": state.attrib["state"],
        }

    except Exception as e:
        raise ParserError(f"NMAP_PARSE_ERROR: {e}")


def parse_naabu_json(data):
    required = ["host", "ip", "port", "protocol"]

    for field in required:
        if field not in data:
            raise ParserError("REQUIRED_FIELD_MISSING")

    return {
        "host": data["host"],
        "ip": data["ip"],
        "port": data["port"],
        "transport": data["protocol"],
    }


def parse_httpx_json(data):
    return {
        "scheme": data["url"].split(":")[0],
        "host": data["url"].split("//")[1].split(":")[0],
        "port": int(data["url"].split(":")[-1]),
        "status": data["status_code"],
    }


def parse_line(text):
    parts = text.split()

    host_port = parts[0]
    ip, port = host_port.split(":")

    return {
        "ip": ip,
        "port": int(port),
        "service": parts[1],
        "product": parts[2],
    }


def parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        raise ParserError("MALFORMED_TOOL_OUTPUT")