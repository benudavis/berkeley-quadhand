"""Remove grid scene nodes from prerecorded Viser files in place."""

from __future__ import annotations

import argparse
from pathlib import Path

import msgspec
import zstandard


def decode_recording(path: Path) -> tuple[dict, list[memoryview]]:
    compressed = path.read_bytes()
    expected_size = int.from_bytes(compressed[:8], "little")
    payload = zstandard.ZstdDecompressor().decompress(
        compressed[8:], max_output_size=expected_size
    )

    metadata_size = int.from_bytes(payload[:8], "little")
    metadata = msgspec.msgpack.decode(payload[8 : 8 + metadata_size])

    offset = 8 + metadata_size
    buffers: list[memoryview] = []
    for buffer_size in metadata["binaryBufferLengths"]:
        offset += (8 - offset % 8) % 8
        buffers.append(memoryview(payload)[offset : offset + buffer_size])
        offset += buffer_size

    return metadata, buffers


def encode_recording(metadata: dict, buffers: list[memoryview]) -> bytes:
    packed_metadata = msgspec.msgpack.encode(metadata)
    parts: list[bytes | memoryview] = [
        len(packed_metadata).to_bytes(8, "little"),
        packed_metadata,
    ]
    offset = 8 + len(packed_metadata)

    for buffer in buffers:
        padding = (8 - offset % 8) % 8
        if padding:
            parts.append(b"\x00" * padding)
            offset += padding
        parts.append(buffer)
        offset += buffer.nbytes

    inner_size = sum(memoryview(part).nbytes for part in parts)
    compressor = zstandard.ZstdCompressor(level=12, threads=-1).compressobj(
        size=inner_size
    )
    output = [inner_size.to_bytes(8, "little")]
    output.extend(compressor.compress(part) for part in parts)
    output.append(compressor.flush())
    return b"".join(output)


def remove_grids(path: Path) -> int:
    metadata, buffers = decode_recording(path)
    grid_names = {
        message[1].get("name")
        for message in metadata["messages"]
        if message[1].get("type") == "GridMessage"
    }
    grid_names.discard(None)

    if not grid_names:
        return 0

    original_count = len(metadata["messages"])
    metadata["messages"] = [
        message
        for message in metadata["messages"]
        if message[1].get("type") != "GridMessage"
        and message[1].get("name") not in grid_names
    ]
    removed_count = original_count - len(metadata["messages"])

    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_bytes(encode_recording(metadata, buffers))

    check_metadata, _ = decode_recording(temporary_path)
    assert not any(
        message[1].get("type") == "GridMessage"
        or message[1].get("name") in grid_names
        for message in check_metadata["messages"]
    )
    temporary_path.replace(path)
    return removed_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("recordings", nargs="+", type=Path)
    args = parser.parse_args()

    for recording in args.recordings:
        removed = remove_grids(recording)
        print(f"{recording}: removed {removed} grid messages")


if __name__ == "__main__":
    main()
