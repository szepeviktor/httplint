from argparse import ArgumentParser, Namespace
import sys
import time

from thor.http.common import Delimiters

from httplint.cli_http_parser import HttpCliParser, modes


def main() -> None:
    args = getargs()
    start_time = int(time.time()) if args.now else None
    parser = HttpCliParser(args, start_time)
    parser.handle_input(sys.stdin.read().encode("utf-8"))
    if parser._input_delimit == Delimiters.CLOSE:
        parser.input_end([])


def getargs() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        choices=[i.value for i in modes],
        default=modes.RESPONSE,
        dest="mode",
        help="The input mode",
    )

    parser.add_argument(
        "-n",
        "--now",
        action="store_true",
        dest="now",
        help="Assume that the HTTP exchange happened now",
    )
    return parser.parse_args()
