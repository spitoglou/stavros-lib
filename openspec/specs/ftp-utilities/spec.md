# FTP Utilities

## Purpose
Provide utilities for uploading files to FTP servers, monitoring local directories for changes, and managing remote directory structures.

## Requirements

### Requirement: FTP Directory Upload
The system SHALL provide a function to upload all files from a local directory to an FTP server.

#### Scenario: Upload directory with file filtering
- **WHEN** user calls `upload_all(server, username, password, local_dir, remote_dir)`
- **THEN** all files in local directory are uploaded to remote directory
- **AND** files matching ignore patterns are excluded
- **AND** remote directory structure is created if it doesn't exist

#### Scenario: Upload with walk option
- **WHEN** user calls `upload_all()` with `walk=True`
- **THEN** function recursively uploads all subdirectories

#### Scenario: Upload with file extension filtering
- **WHEN** user provides ignore_extensions parameter
- **THEN** files with specified extensions are excluded from upload

### Requirement: FTP Directory Monitoring
The system SHALL provide a function to monitor local directory changes and auto-upload modified files.

#### Scenario: Monitor and upload on change
- **WHEN** user calls `monitor_and_ftp(server, username, password, local_dir, remote_dir)`
- **THEN** function monitors local directory for file modifications
- **AND** uploads changed files automatically
- **AND** runs continuously until interrupted

#### Scenario: Detect file modifications
- **WHEN** a file is modified in monitored directory
- **THEN** function detects change by comparing modification times
- **AND** uploads only the changed file

### Requirement: FTP Helper Operations
The system SHALL provide helper functions for common FTP operations.

#### Scenario: Check if remote path exists
- **WHEN** user calls `ftp_helper.path_exists(path)`
- **THEN** function returns True if path exists on FTP server
- **AND** returns False otherwise

#### Scenario: Create remote directory recursively
- **WHEN** user calls `ftp_helper.makedirs(path)`
- **THEN** function creates all parent directories if they don't exist
- **AND** skips creation if directory already exists

### Requirement: Error Handling
The system SHALL handle FTP connection and operation errors gracefully.

#### Scenario: Handle connection failure
- **WHEN** FTP server is unreachable
- **THEN** function logs error and returns False
- **AND** does not crash

#### Scenario: Handle authentication failure
- **WHEN** credentials are invalid
- **THEN** function logs authentication error
- **AND** returns False

### Requirement: Type Safety and Documentation
The system SHALL provide type-hinted functions with clear docstrings.

#### Scenario: Function signatures with type hints
- **WHEN** developer uses IDE with type checking
- **THEN** all parameters and return types are clearly specified
