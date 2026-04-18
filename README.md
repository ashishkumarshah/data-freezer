# data-freezer

`data-freezer` is a CLI tool for incremental file archiving.

## Motivation

One practical reason to use this utility is long-term storage cost: archiving infrequently accessed data to AWS S3
Glacier Deep Archive can be significantly cheaper than paying for a monthly Google Drive or iCloud storage plan.

## What it does

- Scans a source directory.
- Detects files not yet recorded in its local metadata DB.
- Creates a compressed archive (`.tar.gz`) for new files.
- Tracks archived files in SQLite under `.data_freeze`.
- Intended destination is AWS Glacier/Deep Archive.

## Important behavior

- The source directory is never modified.
- You can run this against external hard drives, old PCs, or mounted data volumes safely.
- The work directory can be:
    - on your local device, or
    - on the same external drive.
- You can run the utility repeatedly as new data accumulates; each run archives only what is new/changed.

## Current status

- Local scanning, metadata tracking, and archive creation are implemented.
- Upload is a TODO (`DeepFreezeUtil.upload()` is not implemented yet).

## CLI commands

- `data-freezer setup --source-dir <path> --work-dir <path>`
- `data-freezer archive --source-dir <path> --work-dir <path>` (upload to s3 is a TODO)
- `data-freezer search --pattern <file_name_pattern> --work-dir <path>` (TODO)
- `data-freezer restore --archive-id <id>` (TODO)
- `data-freezer doctor --source-dir <path> --work-dir <path>` (TODO)
