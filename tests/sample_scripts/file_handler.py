<<<<<<< HEAD
"""
Another sample script with file handling functions.
"""

import os
import json

DEFAULT_ENCODING = "utf-8"
BUFFER_SIZE = 8192


def read_file(filepath):
    """Read contents of a file."""
    path = validate_path(filepath)
    with open(path, 'r', encoding=DEFAULT_ENCODING) as f:
        return f.read()


def write_file(filepath, content):
    """Write content to a file."""
    path = validate_path(filepath)
    ensure_directory(os.path.dirname(path))
    with open(path, 'w', encoding=DEFAULT_ENCODING) as f:
        f.write(content)


def append_file(filepath, content):
    """Append content to a file."""
    path = validate_path(filepath)
    with open(path, 'a', encoding=DEFAULT_ENCODING) as f:
        f.write(content)


def delete_file(filepath):
    """Delete a file."""
    path = validate_path(filepath)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def read_json(filepath):
    """Read a JSON file."""
    content = read_file(filepath)
    return parse_json(content)


def write_json(filepath, data):
    """Write data to a JSON file."""
    content = format_json(data)
    write_file(filepath, content)


def parse_json(content):
    """Parse JSON string to object."""
    return json.loads(content)


def format_json(data):
    """Format data as JSON string."""
    return json.dumps(data, indent=2)


def validate_path(filepath):
    """Validate and normalize a file path."""
    if not filepath:
        raise ValueError("Filepath cannot be empty")
    return os.path.normpath(filepath)


def ensure_directory(dirpath):
    """Ensure a directory exists."""
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


def list_files(directory, extension=None):
    """List files in a directory."""
    path = validate_path(directory)
    files = os.listdir(path)
    if extension:
        files = [f for f in files if f.endswith(extension)]
    return files
=======
"""
Another sample script with file handling functions.
"""

import os
import json

DEFAULT_ENCODING = "utf-8"
BUFFER_SIZE = 8192


def read_file(filepath):
    """Read contents of a file."""
    path = validate_path(filepath)
    with open(path, 'r', encoding=DEFAULT_ENCODING) as f:
        return f.read()


def write_file(filepath, content):
    """Write content to a file."""
    path = validate_path(filepath)
    ensure_directory(os.path.dirname(path))
    with open(path, 'w', encoding=DEFAULT_ENCODING) as f:
        f.write(content)


def append_file(filepath, content):
    """Append content to a file."""
    path = validate_path(filepath)
    with open(path, 'a', encoding=DEFAULT_ENCODING) as f:
        f.write(content)


def delete_file(filepath):
    """Delete a file."""
    path = validate_path(filepath)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def read_json(filepath):
    """Read a JSON file."""
    content = read_file(filepath)
    return parse_json(content)


def write_json(filepath, data):
    """Write data to a JSON file."""
    content = format_json(data)
    write_file(filepath, content)


def parse_json(content):
    """Parse JSON string to object."""
    return json.loads(content)


def format_json(data):
    """Format data as JSON string."""
    return json.dumps(data, indent=2)


def validate_path(filepath):
    """Validate and normalize a file path."""
    if not filepath:
        raise ValueError("Filepath cannot be empty")
    return os.path.normpath(filepath)


def ensure_directory(dirpath):
    """Ensure a directory exists."""
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


def list_files(directory, extension=None):
    """List files in a directory."""
    path = validate_path(directory)
    files = os.listdir(path)
    if extension:
        files = [f for f in files if f.endswith(extension)]
    return files
>>>>>>> 12342d4e14c9bffcf018c29ac3a8c2b4ba50b1a9
