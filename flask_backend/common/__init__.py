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


def replace_template_variables(dockerfile, defaults, frontend_dockerfile=None, user_values=None):
    # Process #each directives first
    each_pattern = r"\{\{\#each (.*?)\}\}(.*?)\{\{\/each\}\}"
    each_matches = re.finditer(each_pattern, dockerfile, re.DOTALL)
    for match in each_matches:
        list_variable, content = match.groups()
        items = defaults.get(list_variable.split('.')[1], [])  # assuming format like defaults.list_name
        replacement = ''.join([re.sub(r"\{\{this\}\}", item, content) for item in items])
        dockerfile = dockerfile.replace(match.group(0), replacement)

    # Process #if directives
    if_pattern = r"\{\{\#if (.*?)\}\}(.*?)\{\{\/if\}\}"
    if_matches = re.finditer(if_pattern, dockerfile, re.DOTALL)
    for match in if_matches:
        condition, content = match.groups()
        include_content = False
        if condition == "frontend" and frontend_dockerfile is not None:
            include_content = True
        dockerfile = dockerfile.replace(match.group(0), content if include_content else "")
        
    # Process template variables
    variable_pattern = r"\{\{ (.*?) \}\}"
    variable_matches = re.findall(variable_pattern, dockerfile)
    for variable in variable_matches:
        value = user_values.get(variable, defaults.get(variable, '')) if user_values is not None else defaults.get(variable, '')
        dockerfile = re.sub(r"\{\{\s*" + variable + r"\s*\}\}", value, dockerfile)

    return dockerfile

# Example Usage
user_values = {"version": "3.1", "project_name": "MyApp"}  # Example user provided values
defaults = {"version": "6.0", "project_name": "DefaultProject"}  # Example default values

processed_dockerfile = replace_template_variables(backend_dockerfile, backend_data_test["defaults"], frontend_dockerfile)
print(processed_dockerfile)
