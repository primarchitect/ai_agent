import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # Input normalization
        working_dir_abs: str = os.path.abspath(working_directory)
        file_path_abs:str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Common error handling    
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        # Make any missing directories in target file path
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        # Write file
        with open(file_path_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: writing file content: {e}"  