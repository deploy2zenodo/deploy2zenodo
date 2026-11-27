<!-- markdownlint-disable MD024 -->
# CHANGELOG

## [Unreleased 0.9.0]

### Added

* Support for external configuration files via `DEPLOY2ZENODO_CONFIG` and
  `DEPLOY2INVENIORDM_CONFIG` (defaults: `~/.deploy2zenodo.conf` and
  `~/.deploy2inveniordm.conf`; environment variables take precedence).
* Enhanced security: Access tokens no longer appear in the process argument
  list (`argv`); they are passed to `curl` via a temporary header file.
* Access tokens can now also be provided as a path to a file.
* Startup dependency check for `curl`, `jq`, and `md5sum` (exit code 40
  if any are missing).
* Enhanced the `pre-commit` job to verify and check generated ci templates via
  `yaml2script` with `shellcheck`.
* New CI step to automatically archive releases with Software Heritage.

### Changed

* Optimized `jq` calls and refactored variable loading logic.
* Improved GitLab CI tag extraction and release mirroring jobs.
* Improved compatibility and robustness in regular expressions (`sed` patterns).
* Using `printf` instead of`echo` for enhanced compatibility.
* Enhanced compatibility and robustness in internal tooling script.
* Fixed old files were not deleted in deploy2inveniordm.
* Fixed unique exit code check in test.
* Enhanced documentation.

## [0.8.1] - 2026-11-05

### Added

* New detailed guide on handling API rate limits (`README.rate-limit.md`)
* New GitLab CI jobs for deploying HTML documentation to GitLab Pages and
  notifying release mirrors.
* Added logo in different formats.

### Removed

* `create_pdf` script (replaced by the more versatile `create_doc`).

## [0.8.0] - 2026-10-08

### Added

* Implemented API rate limiting for Zenodo (max 30 req/min), including an
  "auto" mode to calculate safe wait times.
* Added `DEPLOY2INVENIORDM_RATE_LIMIT` and `DEPLOY2ZENODO_RATE_LIMIT`.
* Added colored warning messages in the console.

### Changed

* Improved checksum verification and publication date validation (EDTF).
* Updated logging to ISO 8601 format.

## [0.7.3] - 2026-05-26

### Added

* "Quick start (TL;DR)" section in README with a decision table and CI
  integration examples.

### Changed

* `deploy2inveniordm`: Now automatically attempts to use a draft if a
  record is not found (404).

## [0.7.2] - 2026-05-21

### Added

* `deploy2inveniordm`: Implemented DOI reservation logic and improved
  handling of file upload pathnames.

## [0.7.1] - 2026-05-07

### Changed

* `deploy2inveniordm`: Fixed bugs in deposition ID handling and added
  mandatory API headers for metadata retrieval.

## [0.7.0-beta] - 2026-04-16

### Added

* Introduced `deploy2inveniordm` script for Invenio RDM API deployments.
* Added helper scripts to generate GitLab CI pipelines and standalone
  shell scripts for `deploy2inveniordm`.
* Dedicated documentation for Invenio RDM workflows.

## [0.6.5] - 2025-03-27

### Changed

* Refactored CI pipeline templates for better structure.

### Removed

* `yaml2script.py` (replaced by `yaml2script` pre-commit hook,
  cf. [gitlab.com/yaml2script/yaml2script](https://gitlab.com/yaml2script/yaml2script)).

## [0.6.4] - 2024-11-29

### Added

* Automated download of Zenodo DOI badges as CI artifacts.
* Expanded security guidance on using masked/protected variables for
  trigger tokens.

## [0.6.3] - 2024-10-12

### Added

* Implemented fallback logic for `CONCEPTDOI` and `upload_type` retrieval
  using the record DOI and ID when the `conceptdoi` field is missing.

## [0.6.2] - 2024-10-01

### Added

* `deploy2zenodo`: Implemented `IsPartOf` support for new records.
* Documentation on handling `IsNewVersionOf` in split-step deployments.

## [0.6.1] - 2024-09-30

### Added

* Automatic version referencing: Added `IsNewVersionOf` and `IsPartOf`
  logic via new optional variables.
* Support for "metadata-only" records by automatically uploading a dummy
  file.

## [0.6.0] - 2024-04-02

### Added

* New utility `check_edtf_level_0` to validate publication dates.
* Integrated EDTF validation into `deploy2zenodo`.

## [0.5.5] - 2024-03-13

### Added

* `deploy2zenodo`: Now logs the final `HTMLURL` of the published record.

## [0.5.4] - 2024-01-10

### Added

* Comprehensive logging with timestamps and specific and unique
  exit codes (1-23) for precise error diagnostics.
* Improved JSON handling using `jq -r` to eliminate the need for `sed`.

## [0.5.3] - 2023-11-23

### Added

* New sections on "harvesting" and "curating" (metadata
  strategies, publication workflows).
* Guidance on GitLab UI for environment variables.

## [0.5.2] - 2023-11-16

### Added

* `fix_my_zenodo_record_publication_date` utility script.

## [0.5.1] - 2023-11-13

### Added

* Optional variable `DEPLOY2ZENODO_ADD_IsCompiledBy_DEPLOY2ZENODO` to
  reference the tool in metadata.

## [0.5.0] - 2023-11-11

### Changed

* Major restructuring of the release pipeline into a multi-step proces.
* Automated generation of `README.pdf` and `CITATION.cff` validation.

## [0.4.3] - 2023-11-03

### Added

* New `deploy_to_github` job to mirror repositories via SSH to
  [github.com/deploy2zenodo/deploy2zenodo](https://github.com/deploy2zenodo/deploy2zenodo).

## [0.4.2] - 2023-11-02

### Added

* Configurable curl timeouts iva `DEPLOY2ZENODO_CURL_MAX_TIME` and
  `DEPLOY2ZENODO_CURL_MAX_TIME_PUBLISH`.

## [0.4.1] - 2023-10-30

### Added

* `DEPLOY2ZENODO_SKIP_UPLOAD`: Allows skipping data uploads in
  split-deployment workflows.

## [0.4.0] - 2023-10-30

### Added

* `DEPLOY2ZENODO_SKIP_NEW_VERSION`: Allows updating existing records
  without creating a new version.
* `DEPLOY2ZENODO_GET_METADATA`: Saves the resulting record metadata to
  a file.

## [0.3.1] - 2023-10-30

### Added

* `DRYRUN` and `SKIPRUN` modes for simulating API calls and debugging.
* `DEPLOY2ZENODO_SKIP_PUBLISH`: Allows curating before manual publishing via
   Zenodo webinterface.

## [0.3.0] - 2023-10-30

### Added

* Support for uploading multiple files via space-separated list in
  `DEPLOY2ZENODO_UPLOAD`.

## [0.2.0] - 2023-10-27

### Changed

* Enhanced documentation.

## [0.1.1] -- [0.0.1] - 2023-10-27 -- 2023-10-20

### Added

* Core functionaliti for creating and updating zenodo records.
* GitLab CI trigger jobs for multi-project pipelines for
  testing and deploying to zenodo.org.
* Basic parameter validation and mock functions for testing.
