import os
import re

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