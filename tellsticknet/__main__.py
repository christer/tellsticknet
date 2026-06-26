#!/usr/bin/env python3
"""Interact with Tellstick Net device on local network."""

import argparse
import logging
import re
from datetime import datetime
from sys import argv, stdout, stderr, stdin, version_info
from os.path import join, dirname, expanduser
from os import environ as env
from itertools import product
from yaml import safe_load_all as load_yaml

import asyncio

from tellsticknet import __version__, const
from tellsticknet.protocol import decode_packet
from tellsticknet.controller import discover

from json import dumps as to_json

LOGFMT = "%(asctime)s %(levelname)5s (%(threadName)s) [%(name)s] %(message)s"
DATEFMT = "%y-%m-%d %H:%M.%S"
LOG_LEVEL = logging.DEBUG
_LOGGER = logging.getLogger(__name__)

_ = version_info >= (3, 14) or exit("Python 3.14 required")


def parse_isoformat(s):
    """Parse string with date in ISO 8601 format as datetime

    >>> parse_isoformat("2016-01-15T11:39:15")
    datetime.datetime(2016, 1, 15, 11, 39, 15)
    """
    return datetime(*map(int, re.split("[-:T]", s)))


def parse_stdin():
    """Parse protocol data passed on stdin, previously captured

    example to print all captured sensor id:s
    script/listen > /tmp/packets.log
    cat /tmp/packets.log  | ./script/parse | jq ".sensorId" | sort | uniq
    """
    for line in stdin.readlines():
        line = line.strip()
        if " " in line:
            # assume we have date + raw data separated by space
            timestamp, line = line.split(" ", 1)
            timestamp = parse_isoformat(timestamp)
            lastUpdated = int(timestamp.timestamp())
            packet = decode_packet(line)
            if packet is None:
                continue
            packet.update(lastUpdated=lastUpdated, time=timestamp.isoformat())
            print(to_json(packet))
        else:
            print(to_json(decode_packet(line)))


def prepend_timestamp(line):
    """Add ISO 8601 timestamp to line"""
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    return f"{timestamp} {line}"


async def print_event_stream(controller, raw=False):
    """Print event stream"""

    if raw:
        stream = (prepend_timestamp(packet) async for packet in controller.packets())
    else:
        stream = (to_json(event) async for event in controller.events())

    async for packet in stream:
        print(packet)
        try:
            stdout.flush()
        except OSError:
            # broken pipe
            pass


CONFIG_DIRECTORIES = [
    dirname(argv[0]),
    expanduser("~"),
    env.get("XDG_CONFIG_HOME", join(expanduser("~"), ".config")),
]

CONFIG_FILES = ["tellsticknet.conf", ".tellsticknet.conf"]


def read_config():
    for directory, filename in product(CONFIG_DIRECTORIES, CONFIG_FILES):
        try:
            config = join(directory, filename)
            _LOGGER.debug("checking for config file %s", config)
            with open(config) as config:
                return list(load_yaml(config))
        except OSError:
            continue
    return {}


async def main(args):

    loop = asyncio.get_event_loop()

    def poller(then=None):
        interval = 5
        now = loop.time()
        if then:
            _LOGGER.debug("Poller %f Took %f", interval, now - then)
        loop.call_later(interval, poller, now)

    if loop.get_debug():
        poller()

    cmd = args.command

    if cmd == "parse" and not stdin.isatty():
        parse_stdin()
        exit()
    elif cmd == "mock":
        from tellsticknet.discovery import mock

        await mock()
        exit()
    elif cmd == "devices":
        for e in (e for e in read_config() if "sensorId" not in e):
            print("-", e["name"])
        exit()
    elif cmd == "sensors":
        for e in (e for e in read_config() if "sensorId" in e):
            print("-", e["name"])
        exit()
    elif cmd == "discover":
        async for c in await discover(ip=args.ip, discover_all=True):
            print(c)
        exit()

    config = read_config()
    from functools import partial

    if cmd == "mqtt":
        from tellsticknet.mqtt import run

        await run(partial(discover, ip=args.ip), config)
        exit()

    controller = await discover(ip=args.ip)
    if not controller:
        exit("No tellstick device found")

    _LOGGER.info("Found controller: %s", controller)

    if cmd == "listen":
        await print_event_stream(controller, raw=args.raw)
    elif cmd == "send":
        cmd = args.cmd
        METHODS = dict(
            on=const.TURNON,
            turnon=const.TURNON,
            off=const.TURNOFF,
            turnoff=const.TURNOFF,
            up=const.UP,
            down=const.DOWN,
            stop=const.STOP,
            dim=const.DIM,
        )
        method = METHODS.get(cmd.lower()) or exit("method not found")

        param = args.param

        if method == const.DIM and not param:
            exit("dim level missing")

        name = args.name

        if name:
            devices = [e for e in config if e["name"].lower().startswith(name.lower())]
            if not devices:
                exit(f"Device with name {name} not found")
        else:
            exit("Device name required")

        _LOGGER.info("Executing for %d devices", len(devices))

        _LOGGER.debug("Waiting for tasks to finish")
        await asyncio.gather(
            *[controller.execute(device, method, param=param) for device in devices]
        )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tellsticknet",
        description="Interact with Tellstick Net device on local network",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("-v", action="count", default=0, dest="verbose")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--ip", help="IP of Tellstick Net device")

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("discover", help="Discover Tellstick Net devices")
    sub.add_parser("devices", help="List configured command devices")
    sub.add_parser("sensors", help="List configured sensors")
    sub.add_parser("mqtt", help="Run MQTT bridge")
    sub.add_parser("mock", help="Run mock Tellstick Net device")
    sub.add_parser("parse", help="Parse protocol data from stdin")

    p = sub.add_parser("listen", help="Listen for sensor events")
    p.add_argument("--raw", action="store_true")

    p = sub.add_parser("send", help="Send a command to a device")
    p.add_argument("name", nargs="?", help="Device name")
    p.add_argument("cmd", help="Command: on/off/up/down/stop/dim")
    p.add_argument("param", nargs="?", help="Parameter (e.g. dim level)")

    return parser


def app_main():
    parser = build_parser()
    args = parser.parse_args()

    debug = args.debug
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = [logging.INFO, logging.DEBUG][min(args.verbose, 1)]

    try:
        import coloredlogs

        coloredlogs.install(level=log_level, stream=stderr, datefmt=DATEFMT, fmt=LOGFMT)
    except ImportError:
        _LOGGER.debug("no colored logs. pip install coloredlogs?")
        logging.basicConfig(level=log_level, stream=stderr, datefmt=DATEFMT, format=LOGFMT)

    logging.captureWarnings(debug)

    if debug:
        _LOGGER.info("Debug is on")

    try:
        asyncio.run(main(args), debug=debug)  # pylint: disable=no-member
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    app_main()
