#!/usr/bin/env python3
"""
This is the CLI for the Avro record producer
"""
import argparse
from pathlib import Path

from .emitter import Emitter


def main() -> None:
    """
    Create an argument parser, get our arguments, create an instance of the
    Emitter class with those arguments, and execute the translation.
    """
    parser = argparse.ArgumentParser(
        description="Convert JSON to Avro single-object encoding"
    )
    parser.add_argument("-m", "--message", help="Input message file (JSON)")
    parser.add_argument("-s", "--schema", help="Input schema file (JSON)")
    parser.add_argument("-o", "--output", help="Output Avro file")
    args = parser.parse_args()
    emitter = Emitter(
        schema_file=Path(args.schema),
        message_file=Path(args.message),
        output_file=Path(args.output),
    )
    emitter.emit()
