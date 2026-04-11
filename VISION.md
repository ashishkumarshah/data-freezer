  # Data Freezer - Requirements Specification

## 1. Overview
Data Freezer is a CLI-based archival system that collects unarchived files, compresses them into archives, and uploads them to AWS S3 (Glacier/Deep Archive).

It maintains a local catalog of uploaded data and supports retrieval by archive ID and search by file name.

---

## 2. CLI Commands

### setup
data_freezer setup [--source-dir <path>] [--work-dir <path>]

### archive
data_freezer archive [--source-dir <path>] [--work-dir <path>]

### restore
data_freezer restore --archive-id <id>

### search
data_freezer search --file_name <search_pattern>

### doctor
data_freezer doctor

---

## 3. Work Directory Structure

.data_freeze/
    config.yaml
    db.sqlite
tmp/

---

## 4. Database Schema

### archives
- archive_id
- timestamp
- remote_key
- checksum
- size
- status (PREPARING | PREPARED | UPLOADED | FAILED | NODATA)

### files
- file_path
- hash
- archive_id

---

## 5. Archive Flow

1. Insert archive entry with status = PREPARING
2. Scan source directory and filter unarchived files
3. Insert file entries (file_path, hash, archive_id)
4. Create CSV manifest
5. Create tar archive in work_dir/tmp
6. Update archive status → PREPARED
7. Upload archive → status = UPLOADED
8. Cleanup tar (best effort)

---

## 6. Failure Recovery

Recovery is handled via `doctor`.

Doctor processes all archives not in UPLOADED state:

- PREPARING → continue processing (no rescan)
- PREPARED → retry upload
- FAILED → retry processing

Doctor does NOT modify the files table.

---

## 7. Restore Flow

1. Validate archive_id (must be UPLOADED)
2. Lookup remote_key
3. Initiate restore request
4. Return:
   - retrieval_initiated OR
   - download link

Constraints:
- No local extraction
- No DB updates
- Stateless operation

---

## 8. Search Flow

- Search files table using file_path pattern
- Return archive_ids
- Only include archives where status = UPLOADED

---

## 9. Storage Model

- Backend: AWS S3 (Glacier / Deep Archive)
- One archive = one object
- Retrieval is asynchronous

---

## 10. Design Decisions

- Deduplication: (file_path, hash)
- Same content in different paths is stored separately
- Archive-level restore only
- Stateless restore
- Best-effort snapshot (no file locking)
- No modifications to source directory
- Files table is immutable once written
- Archives are not guaranteed to be complete batches

---

## 11. System Guarantees

### Provided
- Eventual archival of all files
- Deterministic mapping of files → archive_id
- Reliable restore for UPLOADED archives

### Not Provided
- Atomic archive consistency
- Snapshot semantics
- Strong transactional guarantees

---

## 12. Key Invariant

Only archives with:

    status = UPLOADED

are considered valid for:
- search
- restore

---

## 13. System Model Summary

Data Freezer operates as:

- A log-style archival system
- Archives are batching artifacts (not semantic units)
- Completeness is achieved across runs, not per archive
