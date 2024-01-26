import os
import json
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

backend_data_test = json.loads(get_config("asp_net_core", "backends"))
backend_requirements = backend_data_test["requirements"]
backend_dockerfile = ""
for requirement in backend_requirements:
    # print("retreiving requirement: " + requirement)
    # print(backend_data_test[requirement])
    for line in backend_data_test[requirement]:
        backend_dockerfile += line + "\n"
# print(backend_dockerfile)
# print("")
# print("")
# print("")
frontend_data_test = json.loads(get_config("angular", "frontends"))
frontend_requirements = frontend_data_test["requirements"]
frontend_dockerfile = ""
for requirement in frontend_requirements:
    # print("retreiving requirement: " + requirement)
    # print(frontend_data_test[requirement])
    for line in frontend_data_test[requirement]:
        frontend_dockerfile += line + "\n"
# print(frontend_dockerfile)


def replace_template_variables(backend_dockerfile, defaults, frontend_dockerfile=None, frontend_data=None, user_values=None):
    # Function to replace template variables with provided values
    def replace_variables(dockerfile, data_source):
        variable_pattern = r"\{\{ (.*?) \}\}"
        variable_matches = re.findall(variable_pattern, dockerfile)
        for variable in variable_matches:
            value = data_source.get(variable, '')
            dockerfile = re.sub(r"\{\{\s*" + variable + r"\s*\}\}", value, dockerfile)
        return dockerfile

    # Handle #each directives in frontend_dockerfile
    if frontend_dockerfile:
        frontend_dockerfile = process_each_directive(frontend_dockerfile, frontend_data["defaults"])
        frontend_dockerfile = replace_variables(frontend_dockerfile, frontend_data["defaults"])
    
    # Concatenate frontend and backend Dockerfiles
    dockerfile_combined = frontend_dockerfile + backend_dockerfile if frontend_dockerfile else backend_dockerfile

    # Process #each directives in the combined Dockerfile
    dockerfile_combined = process_each_directive(dockerfile_combined, defaults)

    # Process #if directives
    if_pattern = r"\{\{\#if (.*?)\}\}(.*?)\{\{\/if\}\}"
    if_matches = re.finditer(if_pattern, dockerfile_combined, re.DOTALL)
    for match in if_matches:
        condition, content = match.groups()
        if condition == "frontend" and frontend_data:
            content = replace_variables(content, frontend_data.get('defaults', {}))
            dockerfile_combined = dockerfile_combined.replace(match.group(0), content)
        else:
            dockerfile_combined = dockerfile_combined.replace(match.group(0), '')

    # Replace remaining variables in the combined Dockerfile
    dockerfile_combined = replace_variables(dockerfile_combined, user_values if user_values else defaults)

    return dockerfile_combined

def process_each_directive(dockerfile, data_source):
    each_pattern = r"\{\{\#each (.*?)\}\}(.*?)\{\{\/each\}\}"
    each_matches = re.finditer(each_pattern, dockerfile, re.DOTALL)
    for match in each_matches:
        list_variable, content = match.groups()
        items = data_source.get(list_variable.split('.')[1], [])
        replacement = ''.join([re.sub(r"\{\{this\}\}", item, content) for item in items])
        dockerfile = dockerfile.replace(match.group(0), replacement)
    return dockerfile

# Example Usage
user_values = {"version": "3.1", "project_name": "MyApp"}  # Example user provided values

processed_dockerfile = replace_template_variables(backend_dockerfile, backend_data_test["defaults"], frontend_dockerfile, frontend_data_test)
print(processed_dockerfile)
