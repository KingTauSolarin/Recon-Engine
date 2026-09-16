from pathlib import Path


class ReportBuilder:

    def build(self, output_dir, assets):

        html = []

        html.append("<html>")
        html.append("<body>")
        html.append("<h1>Attack Surface Report</h1>")
        html.append("<table border='1'>")

        html.append(
            "<tr><th>Host</th><th>Port</th><th>Service</th></tr>"
        )

        for a in assets:

            html.append(
                f"<tr><td>{a.target}</td><td>{a.port}</td><td>{a.service}</td></tr>"
            )

        html.append("</table>")
        html.append("</body>")
        html.append("</html>")

        Path(output_dir).mkdir(
            exist_ok=True,
            parents=True
        )

        with open(
            Path(output_dir) / "report.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write("\n".join(html))