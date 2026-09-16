import socket
import urllib.request


class Scanner:

    def http_probe(self, host, port):

        url = f"http://{host}:{port}/"

        with urllib.request.urlopen(url, timeout=5) as response:

            return {
                "status": response.status,
                "headers": dict(response.headers),
                "body": response.read().decode("utf-8", errors="replace")
            }

    def line_probe(self, host, port):

        sock = socket.create_connection((host, port), timeout=5)

        data = sock.recv(4096).decode("utf-8", errors="replace")

        sock.close()

        return data