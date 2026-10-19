import http.server, socketserver, subprocess, os

PORT = 7860

def info():
    def run(cmd):
        try:
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode(errors="replace")
        except Exception as e:
            return str(e)
    lines = []
    lines.append("=== Hugging Face Spaces - spek container ===")
    lines.append("CPU (nproc): " + run(["nproc"]).strip())
    lines.append("RAM (free -h):")
    lines.append(run(["free", "-h"]))
    lines.append("ARCH (uname -m): " + run(["uname", "-m"]).strip())
    lines.append("DISK (df -h /):")
    lines.append(run(["df", "-h", "/"]))
    lines.append("USER: " + os.getenv("USER", "?"))
    lines.append("HOSTNAME: " + run(["hostname"]).strip())
    return "\n".join(lines) + "\n"

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = info().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

with socketserver.TCPServer(("0.0.0.0", PORT), H) as httpd:
    httpd.serve_forever()
