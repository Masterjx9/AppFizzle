import os
import re
import json
import zipfile
import shutil

def dockerfile_flow(data_backend, data_frontend=None):
    backend_config = json.loads(get_config(data_backend, "backends"))
    backend_dockerfile = build_dockerfile(backend_config)
    if data_frontend is not None:
        frontend_config = json.loads(get_config(data_frontend, "frontends"))
        frontend_dockerfile = build_dockerfile(frontend_config)
    else:
        frontend_config = None
        frontend_dockerfile = None
    processed_dockerfile = replace_template_variables(backend_dockerfile, backend_config["defaults"], frontend_dockerfile, frontend_config)        
    return processed_dockerfile

def copy_generics(unique_id, framework_name, framework_generics_path, backend_target_directory):
    # Construct the path to the framework's generics directory directly
    generics_dir = os.path.join(os.getcwd(), framework_generics_path, framework_name, "generics")

    # Create a temporary directory with the unique_id
    temp_dir = os.path.join(os.getcwd(), "temp", str(unique_id))
    os.makedirs(temp_dir, exist_ok=True)

    # Copy the backend's src folder to the temporary directory
    backend_src_dir = os.path.join(os.getcwd(), "backends", backend_target_directory, "src")
    if os.path.exists(backend_src_dir):
        shutil.copytree(backend_src_dir, os.path.join(temp_dir, "src"), dirs_exist_ok=True)
    else:
        print(f"Backend src directory not found: {backend_src_dir}")

    # Copy the generics folder to the temporary directory
    if os.path.exists(generics_dir):
        shutil.copytree(generics_dir, os.path.join(temp_dir, "src", "generics"), dirs_exist_ok=True)
        print("Generics folder copied to:", temp_dir)
    else:
        print(f"Generics directory not found: {generics_dir}")

    return temp_dir

def package_dockerfile(unique_id, data, dockerfile):
    if "frontend" in data:
        temp_dir = copy_generics(unique_id, data["frontend"], "frontends", data["backend"])
    else:
        temp_dir = copy_generics(unique_id, data["backend"], "backends", data["backend"])
    
    # Write dockerfile to temporary directory
    dockerfile_path = os.path.join(temp_dir, "src", "dockerfile")
    with open(dockerfile_path, "w") as file:
        file.write(dockerfile)
    
    # Zip the src folder
    zip_path = os.path.join(temp_dir, "src.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(os.path.join(temp_dir, "src")):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, os.path.join(temp_dir, "src")))
    
    packaged_dockerfile = zip_path
    
    return packaged_dockerfile
    
def get_config(folder_name, directory_path):
    directory = os.path.join(os.getcwd(), directory_path)
    for root, dirs, files in os.walk(directory):
        if folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            config_path = os.path.join(folder_path, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    return config_file.read()
    return None

def build_dockerfile(config):
    dockerfile = ""
    for requirement in config["requirements"]:
        for line in config[requirement]:
            dockerfile += line + "\n"
    return dockerfile

def replace_template_variables(backend_dockerfile, backend_defaults, frontend_dockerfile=None, frontend_data=None, user_values=None):
    each_pattern = r"\{\{\#each (.*?)\}\}(.*?)\{\{\/each\}\}"
    if_pattern = r"\{\{\#if (.*?)\}\}(.*?)\{\{\/if\}\}"
    variable_pattern = r"\{\{ (.*?) \}\}"
    
    # Process frontend Dockerfile if provided
    if frontend_dockerfile is not None:
        ft_each_matches = re.finditer(each_pattern, frontend_dockerfile, re.DOTALL)
        for match in ft_each_matches:
            list_variable, content = match.groups()
            items = frontend_data["defaults"].get(list_variable.split('.')[1], [])
            replacement = ''.join([re.sub(r"\{\{this\}\}", item, content) for item in items])
            frontend_dockerfile = frontend_dockerfile.replace(match.group(0), replacement)
        
        ft_variable_matches = re.findall(variable_pattern, frontend_dockerfile)
        for variable in ft_variable_matches:
            value = user_values.get(variable, frontend_data["defaults"].get(variable, '')) if user_values is not None else frontend_data["defaults"].get(variable, '')
            frontend_dockerfile = re.sub(r"\{\{\s*" + variable + r"\s*\}\}", value, frontend_dockerfile)
        
        backend_dockerfile = frontend_dockerfile + backend_dockerfile
    
    # Process backend Dockerfile
    bk_each_matches = re.finditer(each_pattern, backend_dockerfile, re.DOTALL)
    for match in bk_each_matches:
        list_variable, content = match.groups()
        items = backend_defaults.get(list_variable.split('.')[1], [])
        replacement = ''.join([re.sub(r"\{\{this\}\}", item, content) for item in items])
        backend_dockerfile = backend_dockerfile.replace(match.group(0), replacement)

    if_matches = re.finditer(if_pattern, backend_dockerfile, re.DOTALL)
    for match in if_matches:
        condition, content = match.groups()
        if condition == "frontend" and frontend_data is not None:
            while re.search(variable_pattern, content):
                for variable in re.findall(variable_pattern, content):
                    if 'frontend.' in variable:
                        variable_key = variable.split('frontend.')[1]
                        value = frontend_data.get(variable_key, '')
                    else:
                        value = frontend_data["defaults"].get(variable, '') if user_values is None else user_values.get(variable, frontend_data["defaults"].get(variable, ''))
                    content = re.sub(r"\{\{\s*" + variable + r"\s*\}\}", value, content)
            backend_dockerfile = backend_dockerfile.replace(match.group(0), content)
        else:
            # Remove the if block entirely if no frontend data is provided
            backend_dockerfile = backend_dockerfile.replace(match.group(0), '')

    bk_variable_matches = re.findall(variable_pattern, backend_dockerfile)
    for variable in bk_variable_matches:
        value = user_values.get(variable, backend_defaults.get(variable, '')) if user_values is not None else backend_defaults.get(variable, '')
        backend_dockerfile = re.sub(r"\{\{\s*" + variable + r"\s*\}\}", value, backend_dockerfile)

    return backend_dockerfile