import csv
import ipaddress


class ScopeError(Exception):
    pass


class ScopeGuard:

    def __init__(self, scope_file):
        self.allowed = []
        self.request_budget = 240
        self.requests_used = 0
        self.load_scope(scope_file)

    def load_scope(self, scope_file):

        with open(scope_file, newline="", encoding="utf-8") as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                if row["scope"].upper() == "IN":

                    host, port = row["asset"].split(":")

                    self.allowed.append({
                        "host": host,
                        "port": int(port)
                    })

    def validate(self, host, port):

        if self.requests_used >= self.request_budget:
            raise ScopeError("Request budget exceeded")

        ip = ipaddress.ip_address(host)

        if not ip.is_loopback:
            raise ScopeError("Target must be loopback")

        for target in self.allowed:

            if target["host"] == host and target["port"] == int(port):

                self.requests_used += 1
                return True

        raise ScopeError("Target outside authorized scope")