import json
import signal
import socket
import threading
from email.utils import formatdate

import click
import pywf as wf


def handle_json(request: wf.HttpRequest, response: wf.HttpResponse):
    response.add_header_pair("Content-Type", "application/json")
    response.append_body(json.dumps({"message": "Hello, World!"}))


def handle_plaintext(request: wf.HttpRequest, response: wf.HttpResponse):
    response.add_header_pair("Content-Type", "text/plain")
    response.append_body("Hello, World!")


def handle_404(request: wf.HttpRequest, response: wf.HttpResponse):
    response.set_status_code("404")


routes = {"/json": handle_json, "/plaintext": handle_plaintext}


def dispatch(task: wf.HttpTask):
    request = task.get_req()
    response = task.get_resp()
    uri = request.get_request_uri()
    handle = routes.get(uri, handle_404)
    handle(request, response)
    response.add_header_pair("Server", "Sogou Python3 WFHttpServer")
    response.add_header_pair("Date", formatdate(usegmt=True))


@click.command()
@click.option("-p", "--port", default=8080, type=click.INT, help="Port.")
@click.option("-b", "--bind", default="localhost", help="Bind address.")
def main(port, bind):
    server = wf.HttpServer(dispatch)
    stop_event = threading.Event()

    def stop(*args):
        if not stop_event.is_set():
            stop_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, stop)

    code = server.start(socket.AddressFamily.AF_INET, bind, port)
    if code != 0:
        print(f"Start server fail, code={code}")
        sys.exit(code)

    stop_event.wait()
    server.stop()


if __name__ == "__main__":
    main()
