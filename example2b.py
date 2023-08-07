#!/usr/bin/env python3
import scripthelper

logger = scripthelper.getLogger(__name__)


def greet(name):
    logger.info(f"Hello {name}")


def main():
    scripthelper.add_argument("--name", default="World")
    args = scripthelper.initialize()
    greet(args.name)


main()
