# E01 / EWF Evidence Image Research

Purpose: define what Stage 1 must understand about segmented EWF/EnCase images.

Source notes:

- libewf is an open-source library for the Expert Witness Compression Format. It supports EnCase `.E01` and `.Ex01`, provides tools such as `ewfinfo`, `ewfexport`, `ewfmount`, and `ewfverify`, and can expose EWF evidence data for other tooling. Source: https://github.com/libyal/libewf

Key concepts:

- E01 is a forensic evidence container format, not a filesystem.
- Evidence may be segmented across files such as `.E01`, `.E02`, `.E03`, continuing as needed.
- The app should treat the segment chain as one logical evidence stream.
- Metadata may include acquisition notes, case information, examiner information, media size, compression data, sector size, and integrity hashes or checksums depending on the image.
- Verification is separate from opening: the app should distinguish "metadata readable" from "image verified."

Stage 1 intake requirements:

- Accept a path to the first segment, normally `.E01`.
- Identify sibling segment files using the same base name and expected extension sequence.
- Report present segments, missing expected segments, duplicate-looking segments, and unsupported extension patterns.
- Never write to evidence paths.
- Provide an adapter interface so a real libewf/pyewf reader can be swapped in cleanly.
- If libewf/pyewf is not installed, return a clear "adapter unavailable" status rather than crashing.

Metadata output target:

- Evidence id or temporary evidence key.
- Source first segment path.
- Discovered segment list.
- Segment count.
- Segment warnings.
- Reader adapter name and availability.
- Evidence metadata dictionary, if available.
- Verification status: not supported, not run, passed, failed, or error.
- Read-only access assertion.

Review focus:

- Segment discovery should not assume that every missing later segment exists; it should report what it can prove from the folder.
- Real evidence paths should never be hard-coded in tests.
- Tests should use generated empty/mock segment names for discovery and a mocked adapter for metadata shape.
