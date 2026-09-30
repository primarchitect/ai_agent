import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file in a specified file path, including optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of target Python file to be run",
                },
                "args": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "List of optional arguments to be passed to the specified Python file to modify the execution (run)",
                },
            },
            "required": ["file_path"]
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # Input normalization
        working_dir_abs: str = os.path.abspath(working_directory)
        file_path_abs: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Common error handling checks
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        # Prepare the subprocess payload
        command: list[str] = ["python", file_path_abs]
        if args:
            command.extend(args)
        result: subprocess.CompletedProcess = subprocess.run(
            command,
            cwd=working_dir_abs,
            timeout=30,
            check=True,
            capture_output=True,
            text=True,
        )
        # Capture CompletedProcess object output values
        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
