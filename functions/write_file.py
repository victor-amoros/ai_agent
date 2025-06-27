import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(target_file)):
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        except Exception as e:
            return f"Error creating directories: {e}"
    if os.path.exists(target_file) and os.path.isdir(target_file):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f'Succesfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content into an existing file, replacing the old text, or a new one, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file we want to write to, relative to the working directory. If it doesn't exists it should create it, if it exists it will override it.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content we want to write into the file",
            ),
        },
    ),
)