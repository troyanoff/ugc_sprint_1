from gevent import monkey

monkey.patch_all()

import argparse

from gevent.pywsgi import WSGIServer
from src.app import create_app


def main():
    parser = argparse.ArgumentParser(
        description="Run the Flask app with a specific port."
    )
    parser.add_argument(
        "-p", "--port", type=int, default=5000, help="Port to run the Flask app on"
    )
    args = parser.parse_args()

    app = create_app()

    http_server = WSGIServer(("", args.port), app)
    print(f"Starting server on port {args.port}")
    http_server.serve_forever()


if __name__ == "__main__":
    main()
