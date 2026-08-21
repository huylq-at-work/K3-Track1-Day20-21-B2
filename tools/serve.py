#!/usr/bin/env python3
"""Mở các tool trong thư mục này qua http://127.0.0.1:8778

    py tools/serve.py

Vì sao cần: trình duyệt CHẶN quyền ghi đè file khi trang được mở bằng file://
(bấm đúp vào .html). Qua http://127.0.0.1 thì md-editor lưu đè được bằng Ctrl+S.
Không cần API key, không cần cài gì thêm.
"""
import os
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

TOOLS = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("TOOLS_PORT", "8778"))


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/md-editor.html"
        return super().do_GET()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    url = "http://127.0.0.1:%d/" % PORT
    print("Sửa markdown : %s" % url)
    print("Dừng         : Ctrl+C")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT),
                            partial(Handler, directory=TOOLS)).serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
