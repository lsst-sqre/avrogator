"""This class takes a schema file (JSON), a message (JSON, a single dict),
and an output file path, and it transforms the message into Avro binary.
If single_object is specified, it writes the message with Avro magic bytes
and a schema ID at the front.

This is primarily intended to generate test data for the InfluxDB
Telegraf Avro parser plugin.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import fastavro


class Emitter:
    """Class to encapsulate translation functionality."""

    def __init__(
        self,
        schema_file: Optional[Path] = None,
        message_file: Optional[Path] = None,
        output_file: Optional[Path] = None,
        single_object: bool = False,
    ) -> None:
        self.schema: Dict[str, Any] = None
        self.message: Dict[str, Any] = dict()
        self.output_file: Optional[Path] = output_file
        self.single_object = single_object
        if schema_file:
            self.set_schema(schema_file)
        if message_file:
            self.message_from_file(message_file)

    def set_schema(self, schema_file: Path) -> None:
        """Set the schema from a schema JSON file."""
        with open(schema_file, "rb") as f:
            s_obj = json.load(f)
        self.schema = fastavro.parse_schema(s_obj)

    def message_from_file(self, message_file: Path) -> None:
        """Load the input message from a JSON file."""
        with open(message_file, "rb") as f:
            message = json.load(f)
        if type(message) is not dict:
            raise RuntimeError("Message must be dict but got {type(message)}")
        self.message = message

    def emit(self) -> None:
        """Convert the messages and write the output file."""
        if not self.output_file:
            raise RuntimeError("Output file required")
        if not self.schema:
            raise RuntimeError("Schema required")
        with open(self.output_file, "wb") as f:
            if self.single_object:
                fingerprint = fastavro.schema.fingerprint(
                    fastavro.schema.to_parsing_canonical_form(self.schema),
                    "CRC-64-AVRO",
                )
                # Fingerprint is big-endian hex/text, so change that...
                bin_fingerprint = bytearray.fromhex(fingerprint)[::-1]
                avro_magic = b"\xC3\x01"
                f.write(avro_magic)
                f.write(bin_fingerprint)
            fastavro.schemaless_writer(f, self.schema, self.message)
