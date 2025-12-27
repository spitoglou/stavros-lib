# file-utilities Specification

## Purpose
Provide common file and path operations (create directories, read/write files, find files by pattern) to complement existing parsing and PDF modules.

## Requirements

### Requirement: Ensure Directory Exists
The library SHALL provide an `ensure_dir()` function that creates a directory if it does not exist. The function SHALL accept a path string and return a `Path` object.

#### Scenario: Create new directory
- **WHEN** `ensure_dir("/tmp/new_dir")` is called with a non-existent path
- **THEN** the directory is created and a `Path` object is returned

#### Scenario: Directory already exists
- **WHEN** `ensure_dir("/tmp/existing_dir")` is called on an existing directory
- **THEN** no error is raised, and a `Path` object is returned

#### Scenario: Create nested directories
- **WHEN** `ensure_dir("/tmp/a/b/c")` is called with nested non-existent paths
- **THEN** all intermediate directories are created

### Requirement: Read Text File
The library SHALL provide a `read_file()` function that reads a text file and returns its contents as a string. The function SHALL support custom encoding (default: UTF-8).

#### Scenario: Read existing file
- **WHEN** `read_file("config.txt")` is called on an existing file with content "Hello World"
- **THEN** the string "Hello World" is returned

#### Scenario: File not found
- **WHEN** `read_file("nonexistent.txt")` is called on a non-existent file
- **THEN** a `FileNotFoundError` is raised

#### Scenario: Different encoding
- **WHEN** `read_file("latin1.txt", encoding="latin-1")` is called on a file encoded in Latin-1
- **THEN** the content is correctly decoded and returned

### Requirement: Write Text File
The library SHALL provide a `write_file()` function that writes content to a file. The function SHALL support custom encoding (default: UTF-8) and create parent directories if needed.

#### Scenario: Write to new file
- **WHEN** `write_file("output.txt", "Hello World")` is called
- **THEN** a file named "output.txt" is created with the content "Hello World"

#### Scenario: Overwrite existing file
- **WHEN** `write_file("output.txt", "New Content")` is called on an existing file
- **THEN** the file is overwritten with "New Content"

#### Scenario: Create parent directories
- **WHEN** `write_file("new_dir/subdir/output.txt", "Content")` is called with non-existent parent directories
- **THEN** parent directories are created automatically

### Requirement: Find Files by Pattern
The library SHALL provide a `find_files()` function that finds files matching a glob pattern. The function SHALL accept a pattern and optional root directory (default: current directory).

#### Scenario: Find files with extension
- **WHEN** `find_files("*.txt")` is called in a directory with multiple files
- **THEN** a list of all `.txt` files is returned (relative paths)

#### Scenario: Nested pattern matching
- **WHEN** `find_files("**/*.py", root="src")` is called
- **THEN** all Python files in `src/` and subdirectories are returned

#### Scenario: No matches
- **WHEN** `find_files("*.xyz")` is called with no matching files
- **THEN** an empty list is returned

#### Scenario: Invalid root directory
- **WHEN** `find_files("*.txt", root="/nonexistent")` is called
- **THEN** an empty list is returned (or appropriate error handling)
