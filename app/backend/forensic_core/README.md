# Forensic Core

Purpose: core forensic logic.

Stage 1 target:

- E01 segment discovery.
- EWF reader adapter interface.
- Real libewf/pyewf adapter target when available.
- Stub/mock adapter for tests.
- Read-only evidence access assumptions.

Stage 2 target:

- Read-only image/byte-stream abstraction.
- Volume discovery boundary.
- Filesystem adapter boundary.
- Directory metadata and preview foundations.

Stage 2 handoff summary:

- Real local-file backed behavior is limited to `LocalFileImageStream` metadata and bounded reads from tiny local files.
- Volume discovery currently produces a whole-image volume for a readable non-empty stream and does not parse real partition tables.
- Filesystem browsing is adapter-boundary based. The default deterministic tree is stubbed; `pytsk3` remains optional and real parsing is not implemented.
- Preview bytes come from an explicit preview provider. The default provider supplies synthetic bytes for the stub `/hello.txt` entry and does not extract content from a real filesystem.

Stage 3 export-contract start:

- `export_manifest.py` defines JSON-friendly export request, result, manifest, status, warning, content-source identity, source provenance, and hash-placeholder structures.
- S3-T02 adds a backend API export service that writes only explicit provider-backed fixture/stub bytes to examiner-selected output directories.
- S3-T03 verifies written export artifacts by reading the output file after writing, recording on-disk byte count, and computing SHA-256 into the existing `ExportHashSummary` contract.
- S3-T05 documents deleted-file recovery as unsupported/deferred with the current adapters.
- Export content remains separate from Stage 2 metadata and preview rendering. Export bytes must come from an explicit export content source/provider, not from filesystem entries alone and not from rendered preview text or hex.

Stage 4 contract start:

- `content_analysis.py` defines JSON-friendly hash/signature analysis request, result, status, warning, source-provenance, content-source identity, and placeholder digest/signature structures.
- S4-T01 is contract-only. It does not read provider bytes, compute hashes, detect file signatures, persist analysis rows, or claim real evidence-derived analysis.
- S4-T02 adds a Stage 4 analysis content provider boundary and provider-backed hash calculation from explicit provider bytes only.
- S4-T03 adds bounded file signature detection from explicit Stage 4 analysis provider bytes only.
- S4-T04 adds extension mismatch evaluation over reviewed signature results and file name/path metadata only.
- S4-T05 adds fixture-sized known-file matching over reviewed hash results and caller-supplied in-memory records only.
- S4-T06 documents future case-store persistence requirements and keeps current analysis helpers non-persistent.
- S4-T07 reconciles documentation/status only and adds no core behavior.
- Per-file analysis content remains separate from Stage 2 preview rendering, Stage 3 export-output verification, and future whole-image verification.
- Stage 4.5 is the first-testing stage for user-provided E01 files before search/timeline. S4.5-IMP01 is done with a command shell and case-workspace artifact bundle, but real EWF metadata reading, verification, partition parsing, filesystem parsing, and E01-backed file-content providers are not implemented yet.

## S1-T02 Segment Discovery

`discover_e01_segments(path)` accepts a selected first segment path such as `sample.E01` and discovers sibling files with the same base name and `.E##` extensions.

Current behavior:

- accepts `.E01` case-insensitively;
- returns ordered present segments such as `.E01`, `.E02`, `.E03`;
- warns about missing middle segments when a later segment proves a gap;
- returns a structured invalid result for unsupported selected extensions;
- only inspects path names and directory entries, and does not open or parse evidence content.

The result object includes `is_valid_input`, `is_complete`, `read_only`, ordered `segments`, and structured `warnings`. Real EWF metadata reading belongs to a later adapter ticket.

## S1-T03 EWF Reader Adapter

`ewf_reader.py` defines the read-only adapter boundary for EWF metadata and verification:

- `EwfReaderAdapter`: protocol for dependency status, metadata, and verification calls.
- `EwfMetadataResult`: stable metadata result shape with adapter availability, read-only assertion, source paths, metadata, dependency status, verification status, and warnings.
- `VerificationStatus`: stable verification shape using statuses such as `not_supported` and `not_run`.
- `StubEwfReaderAdapter`: dependency-free adapter that returns predictable synthetic metadata for tests.
- `PyewfEwfReaderAdapter`: optional pyewf/libewf adapter skeleton that reports structured dependency-unavailable results when `pyewf` is not installed. If `pyewf` is importable, real metadata extraction is still intentionally unimplemented in Stage 1 and is reported as `real_reader_not_implemented`.

The adapter layer is intentionally separate from segment discovery. Stage 1 does not parse real EWF bytes and does not require real evidence files or native forensic libraries for tests.

## S2-T02 Image Byte-Stream Abstraction

`image_stream.py` defines the first Stage 2 read-only byte access boundary:

- `ImageByteStream`: protocol for stream metadata and bounded byte-range reads.
- `LocalFileImageStream`: local file-backed implementation for tiny generated fixtures and later raw-image experiments.
- `ImageStreamInfo`: source metadata and provenance, including source path, stream type, size, read-only assertion, status, and warnings.
- `ImageReadResult`: bounded read result, including offset, requested length, source size, bytes read, read-only assertion, status, warnings, and raw `bytes` for backend callers.
- `ImageStreamStatus` and `ImageStreamWarning`: structured status/warning objects for normal and error paths.

Current behavior:

- opens local sources only in read-only binary mode;
- supports bounded reads by explicit offset and length;
- reports missing paths, directory paths, unreadable files, invalid negative ranges, and reads beyond the end of the source as structured statuses;
- truncates reads that extend past EOF and emits a `read_truncated_at_eof` warning;
- uses tiny generated files in tests and does not require real evidence, EWF parsing, `pyewf`, libewf, `pytsk3`, or The Sleuth Kit.

S2-T02 does not parse partitions, discover volumes, parse filesystems, list directories, render previews, export files, or hash evidence. Those remain later tickets.

## S2-T03 Volume Discovery Boundary

`volume_discovery.py` defines the first Stage 2 volume result boundary:

- `discover_volumes(stream, strategy="whole_image")`: returns JSON-friendly volume discovery results for an `ImageByteStream`.
- `VolumeDiscoveryResult`: source-level result with schema version, source path, stream type, source size, read-only assertion, strategy, status, volumes, and warnings.
- `VolumeInfo`: one volume-like range with volume id, index, source provenance, offset, length, type, description, read-only assertion, status, and warnings.
- `VolumeDiscoveryStatus` and `VolumeDiscoveryWarning`: structured status/warning objects for normal, unavailable, empty, and unsupported paths.

Current behavior:

- emits one `whole_image` volume for a readable non-empty local file stream;
- returns `empty_image` with no volumes for a zero-byte source;
- returns `image_stream_unavailable` with stream-status warning details for missing, directory, unreadable, or otherwise unavailable image streams;
- returns `partition_parsing_unsupported` for non-`whole_image` strategies so future real partition parsers have a documented boundary.

S2-T03 does not parse real partition tables, parse filesystems, list directories, render previews, export files, hash evidence, or require `pytsk3`, The Sleuth Kit, `pyewf`, libewf, or real forensic images.

## S2-T04 Filesystem Adapter Boundary

`filesystem_adapter.py` defines the Stage 2 filesystem adapter boundary:

- `FilesystemAdapter`: protocol for read-only filesystem metadata adapters.
- `StubFilesystemAdapter`: dependency-free deterministic adapter for tests and later directory-listing integration.
- `Pytsk3FilesystemAdapter`: optional pytsk3 skeleton that reports structured dependency status without requiring `pytsk3`.
- `FilesystemResult`: source/volume-level result with adapter name, dependency status, source path, volume id, volume offset/length, filesystem type, read-only assertion, root path, entries, status, and warnings.
- `FilesystemEntry`: file/directory metadata shape for later S2-T05 listing, including file id, path, name, type, size, allocation/deleted state, timestamps, source provenance, adapter name, read-only assertion, status, and warnings.

Current behavior:

- stub adapter returns deterministic root entries for `/Documents` and `/hello.txt`;
- stub entries are allocated and not deleted;
- pytsk3 adapter returns `dependency_unavailable` when `pytsk3` is missing;
- importable pytsk3 remains `real_parser_not_implemented` until a later ticket intentionally adds real parsing;
- tests do not require real evidence, real filesystems, `pytsk3`, or The Sleuth Kit.

S2-T04 does not add a directory-listing command/workflow, parse real filesystems, render previews, export files, recover deleted files, hash evidence, or require native forensic dependencies. `FilesystemEntry.allocated` and `FilesystemEntry.deleted` are metadata fields only; they do not expose recoverable byte ranges or content providers.

## S2-T05 Directory Listing And File Metadata View

The backend API layer in `app/backend/api/directory_listing.py` consumes the S2-T04 filesystem adapter boundary and exposes a JSON-friendly directory listing callable:

- `list_directory(volume, directory_path="/", adapter=None)`: returns a stable dictionary for a directory listing.
- `directory_listing_to_json(...)`: serializes the listing result for command/API consumers.

Current behavior:

- uses adapter-provided `FilesystemEntry` metadata without mutating adapter results;
- preserves source path, volume id, volume offset/length, filesystem type, adapter/dependency information, read-only assertion, entry status/warnings, allocation/deleted state, and timestamps;
- root listing with `StubFilesystemAdapter` returns `/Documents` and `/hello.txt`;
- non-root directories return `path_unsupported`, files return `path_not_directory`, unknown paths return `path_not_found`, and dependency-unavailable/not-implemented adapters return `filesystem_unavailable`.

S2-T05 does not read file content, render previews, parse real filesystems, export/recover files, compute hashes, add UI, or require native forensic dependencies. Raw/text/hex preview remains S2-T06.

## S2-T06 Raw/Text/Hex Preview Foundation

The backend API layer in `app/backend/api/file_preview.py` provides a bounded preview foundation:

- `preview_file(entry, mode="text", ...)`: returns a JSON-friendly preview result for explicit provider-backed bytes.
- `preview_file_to_json(...)`: serializes preview results for command/API consumers.
- `StubPreviewProvider`: dependency-free provider that maps the synthetic stub file `stub-file-hello` (`/hello.txt`) to `Hello, world!`.

Current behavior:

- supports `raw`, `text`, and `hex` modes;
- preserves source path, volume id, volume offset/length, file id/path/name/type, read-only assertion, provider name, offsets, requested length, returned byte count, source content size, truncation flag, status, and warnings;
- uses JSON-friendly raw byte values, UTF-8 text with visible replacement warnings, and deterministic lowercase hex;
- returns structured statuses for `ok`, `preview_truncated`, `content_unavailable`, `file_not_found`, `path_not_file`, `unsupported_preview_mode`, and `invalid_range`.

S2-T06 does not perform real filesystem byte extraction. The current stub filesystem entries remain metadata-only; preview bytes come from an explicit stub provider. S2-T06 also does not export/recover files, compute hashes, add UI, persist case data, parse real filesystems, or require native dependencies.

## S3-T01 Export Result And Manifest Contract

`export_manifest.py` provides the first Stage 3 export contract boundary:

- `ExportSourceProvenance`: source fields copied from Stage 2-style filesystem entries, including source path, volume id/offset/length, file id/path/name, filesystem type, adapter name, read-only assertion, allocation/deleted state, optional evidence/case ids, and timestamps.
- `ExportContentSourceIdentity`: explicit provider/source identity for future export bytes, including provider name, source kind such as `stub` or later `real_parser`, read-only assertion, synthetic flag, source content size, parser fields, and source status.
- `ExportRequest`: request shape for a future export service, with destination fields and destination-safety status placeholders.
- `ExportResult` and `ExportManifest`: result/manifest shapes with source provenance, content-source identity, output/manifest path placeholders, byte-count placeholders, SHA-256 placeholder, destination status, UTC timestamps, and warnings.
- `ExportStatus`, `ExportWarning`, `ExportHashSummary`, `export_result_to_json()`, and `export_manifest_to_json()` support stable JSON serialization.

Current S3-T01 behavior:

- supports contract serialization only;
- records `export_not_started`, `content_source_unavailable`, `destination_not_checked`, and `hash_not_computed` states without implying file writes or verification;
- uses UTC ISO timestamps ending in `Z`;
- keeps default tests dependency-free and free of real evidence.

S3-T01 does not write exported files or manifest files, compute SHA-256, enforce destination safety, add an API command, persist audit events, implement deleted-file recovery, parse real EWF/partition/filesystem data, or use preview-rendered text/hex as export bytes.

## S3-T02 Fixture/Stub File Export Service

The backend API layer in `app/backend/api/file_export.py` provides the first write-capable Stage 3 export foundation:

- `ExportContentProvider`: protocol for raw export byte providers, intentionally separate from preview providers.
- `StubExportContentProvider`: dependency-free provider that maps the synthetic stub file `stub-file-hello` (`/hello.txt`) to raw `Hello, world!` bytes.
- `export_file(entry_or_request, output_directory, ...)`: validates the source, destination, output name, and provider content; writes the output file and manifest when safe; returns an S3-T01 `ExportResult`.
- `export_file_to_json(...)`: runs export and serializes the returned result as stable JSON.

Current S3-T02 behavior:

- requires an explicit output directory;
- rejects output directories that overlap the known source/evidence path when that can be determined;
- rejects path traversal, unsafe output names, directory/non-file entries, missing content, and existing output/manifest files with structured statuses;
- writes a manifest from `ExportResult.to_manifest()` beside the exported file.

S3-T02 does not parse real filesystems, extract real evidence bytes, add case-store audit integration, implement deleted-file recovery, add UI, or require native forensic dependencies.

## S3-T03 Export Hashing And Byte-Count Verification

The backend API export service now fills the S3-T01 hash and byte-count fields for written artifacts:

- `bytes_requested` remains the provider byte count when known;
- `bytes_written` is measured by reading the written output file after export;
- `ExportHashSummary.sha256` is computed from the written output bytes;
- `ExportHashSummary.status` is `ok` only when SHA-256 was computed from the exported artifact;
- byte-count mismatches return structured `byte_count_mismatch` status and warnings;
- unreadable or missing output after write returns structured `export_verification_failed` with hash status `hash_failed`.

This is export-output verification only. Broader file hash analysis, MD5/SHA-1 production hashing, known-file matching, file signatures, extension mismatch checks, image verification, audit integration, deleted recovery, UI, and real parser work remain deferred.

## S4-T01 Hash And Signature Analysis Contracts

`content_analysis.py` provides the first Stage 4 contract boundary:

- `AnalysisSourceProvenance`: source fields copied from Stage 2-style filesystem entries, including source path, optional case/evidence ids, volume id/offset/length, file id/path/name, entry type, allocation/deleted state, filesystem type, adapter name, read-only assertion, and timestamps.
- `AnalysisContentSourceIdentity`: explicit provider/source identity for future analysis bytes, including provider name, source kind such as `synthetic`, `generated_fixture`, `local_stream`, `export_provider`, or future `real_parser`, read-only assertion, synthetic/generated flags, source content size, source status, parser/source name, and version fields.
- `HashAnalysisRequest`, `HashAnalysisResult`, and `HashDigestResult`: hash-analysis placeholders with requested algorithms, nullable bytes analyzed, per-algorithm nullable digests, status, warnings, and timestamps.
- `SignatureAnalysisRequest` and `SignatureAnalysisResult`: signature-analysis placeholders with max bytes requested, nullable bytes inspected, nullable detected type/signature/MIME fields, status, warnings, and timestamps.
- `AnalysisStatus`, `AnalysisWarning`, and JSON helpers support stable serialization.

Current S4-T01 behavior:

- defines contracts and serialization only;
- records placeholder statuses such as `analysis_not_started`, `hash_not_computed`, `signature_not_checked`, `content_source_unavailable`, `metadata_only_source`, and `preview_rendering_not_allowed`;
- labels synthetic and generated fixture source identities explicitly;
- keeps default tests dependency-free and free of real evidence.

S4-T01 does not compute hashes, detect signatures, read preview/export/provider bytes, treat filesystem metadata as byte-bearing, change Stage 3 export verification, claim whole-image verification, add known-file matching, persist analysis results, add UI/search/timeline/reporting, parse real evidence/filesystems, recover deleted files, carve data, or require native dependencies.

## S4-T02 Provider-Backed Hashing

`content_analysis.py` now provides provider-backed hash behavior while keeping analysis bytes separate from preview and export flows:

- `AnalysisContent`: provider-owned raw bytes plus source identity fields.
- `AnalysisContentProvider`: protocol for explicit Stage 4 analysis byte providers.
- `StubAnalysisContentProvider`: dependency-free provider for synthetic or generated fixture bytes.
- `hash_file_content(...)` and `calculate_hashes(...)`: compute hashes and return the existing `HashAnalysisResult` contract.

Current S4-T02 behavior:

- computes SHA-256 by default from explicit analysis-provider bytes;
- computes MD5 and SHA-1 only when explicitly requested;
- normalizes algorithm names case-insensitively, including `sha-256`/`sha_1` style variants;
- validates requested algorithms before reading provider content;
- returns structured non-ok results for unsupported algorithms, empty or malformed algorithm requests, directory/non-file entries, missing providers, unavailable provider content, and provider exceptions;
- preserves source provenance, content-source identity, source kind, source status, byte count, read-only assertion, timestamps, and warnings;
- labels synthetic and generated fixture bytes with `synthetic_content` or `generated_fixture_content` warnings.

S4-T02 does not detect file signatures, add extension mismatch checks, match known-file sets, persist analysis results, change Stage 3 export-output verification, use preview-rendered text/hex, use export providers or written export artifacts as analysis bytes, claim whole-image verification, parse real evidence/filesystems, recover deleted files, carve data, add UI/search/timeline/reporting, or require native dependencies.

## S4-T03 File Signature Detection

`content_analysis.py` now provides bounded provider-backed file signature detection:

- `FileSignatureDefinition`: one conservative magic-byte definition.
- `SUPPORTED_FILE_SIGNATURES`: dependency-free table for PDF, PNG, JPEG, GIF87a/GIF89a, ZIP header variants, ELF, and MZ executable candidates.
- `detect_file_signature(...)` and `analyze_file_signature(...)`: inspect only `AnalysisContent.data[:max_bytes]` and return `SignatureAnalysisResult`.

Current S4-T03 behavior:

- reuses the S4-T02 `AnalysisContentProvider` boundary;
- validates `max_bytes` before provider reads;
- rejects directory/non-file entries before provider reads;
- reports `metadata_only_source` when no provider is supplied;
- reports `content_source_unavailable` when the provider has no bytes;
- reports `content_provider_error` without raw tracebacks when a provider raises;
- reports `insufficient_signature_bytes` for a bounded prefix that is only a partial known signature;
- reports `unknown_signature` when enough inspected bytes do not match the supported table;
- preserves source provenance, content-source identity, source kind/status, max bytes requested, bytes inspected, read-only assertion, timestamps, and warnings.

MZ results are labeled as `mz_executable_candidate`, not as validated PE files. S4-T03 does not add extension mismatch checks, known-file matching, MIME database integration, persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, export-output behavior changes, or Stage 5 work.

## S4-T04 Extension Mismatch Rules

`content_analysis.py` now provides extension/signature mismatch evaluation without adding another byte source:

- `SignatureExtensionRule`, `SIGNATURE_EXTENSION_RULES`, and `SUPPORTED_SIGNATURE_EXTENSIONS` define a conservative dependency-free allow-list for detected signature types.
- `ExtensionMismatchResult` records source provenance, content-source identity, signature status, detected type/signature/MIME fields, observed extension, expected extensions, explicit `mismatch`, timestamps, and warnings.
- `evaluate_extension_mismatch(...)` and `check_extension_mismatch(...)` consume an existing `SignatureAnalysisResult`; they do not accept providers, read bytes, or call signature detection internally.
- `extension_mismatch_result_to_json(...)` serializes the result shape as stable JSON.

Current S4-T04 behavior:

- normalizes a dot-prefixed lowercase extension from `source.file_name`, falling back to `source.file_path` when needed;
- treats `.PDF` and other mixed-case extensions case-insensitively;
- supports rules for PDF, PNG, JPEG variants, GIF, ZIP containers such as `.docx`, ELF, and conservative MZ executable candidates;
- returns `extension_match` or `extension_mismatch` only when the source is a file, signature status is `ok`, a detected type is present, the detected type has a rule, and file metadata provides an extension;
- returns not-evaluated states such as `path_not_file`, `signature_not_available`, `unsupported_signature_type`, `file_name_unavailable`, or `extension_missing` with `mismatch=None` when required inputs are missing.

S4-T04 does not change S4-T02 hashing, S4-T03 signature detection, preview/export behavior, known-file matching, persistence, search/timeline, UI/reporting, real parser work, deleted recovery, carving, native dependencies, export-output behavior, or Stage 5 work.

## S4-T05 Fixture-Sized Known-File Matching

`content_analysis.py` now provides a small known-file matching foundation without adding another byte source:

- `KnownFileRecord` captures a caller-supplied known-file digest record with `known_good`, `known_bad`, or `known_unknown` category values plus dataset and metadata fields.
- `KnownFileMatchResult` preserves the reviewed hash result's source provenance, content-source identity, hash status, digest statuses, bytes analyzed, timestamps, and warnings.
- `match_known_file_hashes(...)` and `match_known_files(...)` consume only an existing `HashAnalysisResult` plus tiny caller-supplied in-memory records.
- `known_file_match_result_to_json(...)` serializes the result as stable JSON-safe output.

Current S4-T05 behavior:

- matches only digest values already computed on the hash result;
- supports SHA-256, MD5, and SHA-1 records with S4-T02-style algorithm normalization;
- compares digests case-insensitively;
- prefers SHA-256 for top-level match fields when multiple algorithms match, while preserving all matched records;
- returns structured no-match, unavailable-hash, missing-digest, invalid-record, and conflicting-category statuses;
- keeps synthetic/generated content-source labels and adds context warnings when a match came from synthetic or generated fixture hash bytes.

S4-T05 does not accept analysis providers, read bytes, calculate hashes, read known-file lists from disk or network, import NSRL-scale datasets, persist results, add search/timeline behavior, change S4-T02/S4-T03/S4-T04 behavior, parse real evidence/filesystems, recover deleted files, carve data, require native dependencies, or start Stage 5 work.

## S4-T06 Case-Store Persistence Plan

S4-T06 is planning/documentation-only. The Stage 4 result shapes are stable enough to describe future persistence, but `content_analysis.py` still does not write to SQLite or accept persistence context.

Current behavior remains non-persistent:

- `hash_file_content()` / `calculate_hashes()` return `HashAnalysisResult` only;
- `detect_file_signature()` / `analyze_file_signature()` return `SignatureAnalysisResult` only;
- `evaluate_extension_mismatch()` / `check_extension_mismatch()` return `ExtensionMismatchResult` only;
- `match_known_file_hashes()` / `match_known_files()` return `KnownFileMatchResult` only.

Future persistence should be explicit opt-in and should not be triggered by `case_id` or `evidence_id` values embedded in source provenance. A later workflow/API/job layer should provide a SQLite connection, explicit case id, optional evidence id, optional actor/examiner, optional analysis job id, caller intent to persist, and a policy for successful, failed, partial, and not-evaluated results.

Future rows must preserve source provenance, content-source identity, source kind, synthetic/generated flags, status JSON, full result JSON with `schema_version`, warnings, timestamps, and provider/parser names and versions. The recommended schema direction is a parent `analysis_results` table plus optional child/index tables for hash digests, signature detections, extension mismatch flags, and known-file match categories.

S4-T06 does not add schema migrations, persistence helpers, API wrappers, background jobs, search/timeline/reporting, UI, external known-file dataset storage, real parser work, native dependencies, or Stage 5 work.

## S4-T07 Documentation Handoff

S4-T07 is documentation/status reconciliation only. The final Stage 4 behavior remains in `content_analysis.py`: contracts, provider-backed hashes, bounded signatures, extension mismatch over existing signature results, fixture-sized known-file matching over existing hash results, and persistence planning only.

Stage 4 still does not include real EWF, partition, or filesystem parsing; real filesystem file-content extraction; whole-image verification; analysis-result persistence implementation; Stage 4 API wrappers; search/timeline/reporting/UI; external known-file datasets or NSRL import; deleted recovery/carving; or required native dependencies. Stage 5 remains rough/draft and must preserve source/provenance/status/warning/source-kind uncertainty and synthetic/generated/provider-backed labels before building search or timeline behavior.

## S3-T05 Deleted-File Recovery Plan

Deleted-file recovery is not implemented in the current backend. The current distinction is:

- Active allocated file export: S3-T02 through S3-T04 can export explicit provider-backed bytes for a selected file entry, write a manifest, verify SHA-256/byte count, and optionally audit the export.
- Deleted entry metadata: a future filesystem adapter may report that a directory entry is deleted or unallocated, but metadata alone does not prove that file content is recoverable.
- Deleted-file recovery: a future adapter must expose deleted-entry provenance plus recoverable content ranges or an explicit recovery content provider, then route recovered bytes through the existing export/manifest/hash/audit workflow.
- Carving or unallocated-space recovery: scanning unallocated space for signatures/fragments is a separate later capability and is not part of Stage 3.
- Unsupported or unrecoverable entries: if an adapter can see metadata but cannot supply reliable content, the result must be explicit rather than pretending recovery succeeded.

Current project truth:

- `StubFilesystemAdapter` returns only allocated, non-deleted synthetic entries.
- Current filesystem entries are metadata-only and do not carry byte runs, extents, clusters, or recovery handles.
- Preview and export bytes come from explicit synthetic providers only when a file id is registered.
- Current export is active provider-backed export, not deleted-file recovery.
- `Pytsk3FilesystemAdapter` does not parse real filesystems, deleted entries, or recoverable bytes.

Future deleted-recovery adapters must provide:

- allocation/deleted state and filesystem-specific provenance;
- recoverable content ranges, extents, or an explicit content-source/provider identity;
- completeness and confidence status;
- warnings for overwritten, sparse, partial, unavailable, or conflicting ranges;
- read-only source handling;
- compatibility with existing export output, manifest, SHA-256/byte-count verification, and optional audit logging.

Suggested future status/warning names include `deleted_recovery_unsupported`, `deleted_entry_metadata_only`, `recovery_content_unavailable`, `recovery_partial`, `recovery_not_attempted`, and `carving_deferred`.
