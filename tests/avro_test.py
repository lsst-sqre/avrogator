from pathlib import Path

import avrogator


def test_emit(testdata: Path) -> None:
    test_output = Path(testdata / "test_output.avro")
    emitter = avrogator.Emitter(
        schema_file=Path(testdata / "schema.avsc"),
        message_file=Path(testdata / "message.json"),
        output_file=test_output,
    )
    emitter.emit()
    with open(test_output, "rb") as f:
        actual = f.read()
    with open(Path(testdata / "output.avro"), "rb") as f:
        expected = f.read()
    assert actual == expected
