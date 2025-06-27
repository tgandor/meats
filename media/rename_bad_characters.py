import os
import json
import argparse
import sys


def sanitize_filename(filename, keep_spaces=True):
    """
    Remove bad characters from filename.
    Bad characters are defined as any character that is not alphanumeric, a space (optional), a dot, or an underscore.
    """
    allowed_chars = "_.-@+=[]()"
    if keep_spaces:
        allowed_chars += " "
    return "".join(c if c.isalnum() or c in allowed_chars else "_" for c in filename)


def generate_unique_filename(directory, desired_name):
    """
    Generate a unique filename to avoid conflicts.
    If the desired name exists, append a number.
    """
    if not os.path.exists(os.path.join(directory, desired_name)):
        return desired_name

    name, ext = os.path.splitext(desired_name)
    counter = 1
    while True:
        new_name = f"{name}_{counter}{ext}"
        if not os.path.exists(os.path.join(directory, new_name)):
            return new_name
        counter += 1


def save_undo_info(undo_file, operations):
    """Save rename operations to undo file."""
    try:
        with open(undo_file, "w", encoding="utf-8") as f:
            json.dump(operations, f, indent=2, ensure_ascii=False)
        print(f"Undo information saved to {undo_file}")
    except Exception as e:
        print(f"Warning: Could not save undo information: {e}")


def perform_undo(undo_file):
    """Undo previous rename operations."""
    if not os.path.exists(undo_file):
        print(f"Undo file {undo_file} not found.")
        return False

    try:
        with open(undo_file, "r", encoding="utf-8") as f:
            operations = json.load(f)

        if not operations:
            print("No operations to undo.")
            return True

        # Reverse the operations
        failed_operations = []
        for op in reversed(operations):
            old_path = op["new_path"]  # What we renamed to
            new_path = op["old_path"]  # Original name

            if os.path.exists(old_path):
                if os.path.exists(new_path):
                    print(f"Cannot undo: {new_path} already exists")
                    failed_operations.append(op)
                else:
                    os.rename(old_path, new_path)
                    print(
                        f"Undone: {os.path.basename(old_path)} -> {os.path.basename(new_path)}"
                    )
            else:
                print(f"Cannot undo: {old_path} no longer exists")
                failed_operations.append(op)

        if failed_operations:
            print(f"\n{len(failed_operations)} operations could not be undone.")
            return False
        else:
            # Remove the undo file if all operations were successful
            os.remove(undo_file)
            print(
                f"\nAll operations undone successfully. Undo file {undo_file} removed."
            )
            return True

    except Exception as e:
        print(f"Error reading undo file: {e}")
        return False


def rename_bad_characters(directory, keep_spaces=True, undo_file=None):
    """
    Rename files in the specified directory to remove bad characters.
    Only processes regular files, not directories.
    """
    operations = []

    try:
        entries = os.listdir(directory)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
        return False

    for filename in entries:
        file_path = os.path.join(directory, filename)

        # Only process regular files
        if not os.path.isfile(file_path):
            continue

        new_filename = sanitize_filename(filename, keep_spaces)

        if new_filename != filename:
            # Generate unique filename to avoid conflicts
            unique_filename = generate_unique_filename(directory, new_filename)

            old_file_path = file_path
            new_file_path = os.path.join(directory, unique_filename)

            try:
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} -> {unique_filename}")

                # Record operation for undo
                operations.append(
                    {
                        "old_path": old_file_path,
                        "new_path": new_file_path,
                        "old_name": filename,
                        "new_name": unique_filename,
                    }
                )

            except OSError as e:
                print(f"Error renaming {filename}: {e}")

    # Save undo information if any operations were performed
    if operations and undo_file:
        save_undo_info(undo_file, operations)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Rename files to remove bad characters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/files                    # Keep spaces, save undo info
  %(prog)s /path/to/files --no-spaces       # Replace spaces with underscores
  %(prog)s --undo /path/to/files             # Undo previous operations
  %(prog)s /path/to/files --no-undo         # Don't save undo information
        """,
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to process (default: current directory)",
    )
    parser.add_argument(
        "--no-spaces",
        action="store_true",
        help="Replace spaces with underscores instead of keeping them",
    )
    parser.add_argument(
        "--undo", action="store_true", help="Undo previous rename operations"
    )
    parser.add_argument(
        "--no-undo", action="store_true", help="Do not save undo information"
    )

    args = parser.parse_args()

    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        sys.exit(1)

    # Determine undo file path
    undo_file = (
        None if args.no_undo else os.path.join(args.directory, "rename_undo.json")
    )

    if args.undo:
        # Perform undo operation
        if not undo_file:
            undo_file = os.path.join(args.directory, "rename_undo.json")
        success = perform_undo(undo_file)
        sys.exit(0 if success else 1)
    else:
        # Perform rename operation
        keep_spaces = not args.no_spaces
        success = rename_bad_characters(args.directory, keep_spaces, undo_file)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
