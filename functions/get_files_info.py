import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir:str = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return (f'Error: "{directory}" is not a directory')
        files_info: list[str] = []
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(f" - {file_name}: file_size={file_size}, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: listing files: {e}"  


        
        