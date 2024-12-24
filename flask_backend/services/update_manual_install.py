import requests
import json
import os
from common import get_config

def get_latest_installer_link(framework):
    """Fetch the latest installer or installation command for a given framework."""
    installer_sources = {
        "django": "https://pypi.org/pypi/Django/json",
        "flask": "https://pypi.org/pypi/Flask/json",
        "dotnet": "https://dotnet.microsoft.com/en-us/download/dotnet",
        "node": "https://nodejs.org/dist/latest/",
        "ruby": "https://www.ruby-lang.org/en/downloads/",
        "php": "https://www.php.net/downloads.php",
        "java": "https://jdk.java.net/",
        "elixir": "https://elixir-lang.org/install.html",
        "erlang": "https://www.erlang.org/downloads",
        "perl": "https://www.perl.org/get.html",
        "haskell": "https://www.haskell.org/platform/",
        "shiny": "https://cran.r-project.org/web/packages/shiny/index.html",
        "lucee": "https://download.lucee.org/"
    }

    url = installer_sources.get(framework)
    if not url:
        raise Exception(f"No installer source found for framework: {framework}")

    # For PyPI-based frameworks like Django or Flask
    if "pypi.org" in url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["urls"][0]["url"]  # Return the first download link
        else:
            raise Exception(f"Failed to fetch installer for {framework} from PyPI.")

    # For Node.js or other sites with predictable patterns
    if "nodejs.org" in url:
        return f"{url}node-v{get_latest_node_version()}-linux-x64.tar.xz"

    # For other frameworks, just return the official page
    return url


def update_config_with_installers():
    """Update each backend's config.json with manual installation links."""
    framework_mapping = {
        "django": "django",
        "flask": "flask",
        "sinatra": "ruby",
        "ruby-on-rails": "ruby",
        "spring-boot": "java",
        "micronaut": "java",
        "quarkus": "java",
        "akka-http": "java",
        "play-framework": "java",
        "ktor": "java",
        "adonis": "node",
        "meteorjs": "node",
        "laravel": "php",
        "codeigniter": "php",
        "symfony": "php",
        "asp_net_core": "dotnet",
        "blazor": "dotnet",
        "cowboy": "erlang",
        "dancer": "perl",
        "yesod": "haskell",
        "shiny": "shiny",
        "phoenix": "elixir",
        "coldfusion": "lucee"
    }

    for folder_name, framework in framework_mapping.items():
        try:
            # Fetch the latest installer link
            installer_link = get_latest_installer_link(framework)
            print(f"Installer link for {folder_name}: {installer_link}")

            # Get the current config.json content
            config_content = get_config(folder_name, "backends")
            if config_content is None:
                print(f"No config.json found for {folder_name} in 'backends'. Skipping.")
                continue

            # Parse the config and update with the installer link
            config = json.loads(config_content)
            if "defaults" not in config:
                config["defaults"] = {}
            config["defaults"]["manual_installer"] = installer_link

            # Write the updated config.json back to the respective folder
            directory_path = os.path.join(os.getcwd(), "backends", folder_name)
            config_path = os.path.join(directory_path, "config.json")
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)
            print(f"Updated config.json for {folder_name}")

        except Exception as e:
            print(f"Error updating {folder_name}: {e}")


# Helper function for Node.js
def get_latest_node_version():
    """Fetch the latest Node.js version."""
    url = "https://nodejs.org/dist/index.json"
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json()
        return versions[0]["version"].lstrip("v")  # Return the latest version
    else:
        raise Exception("Failed to fetch Node.js versions.")
update_config_with_installers()