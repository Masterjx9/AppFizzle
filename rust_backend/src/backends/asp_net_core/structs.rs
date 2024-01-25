use serde::{Serialize, Deserialize};
use serde_json;
use std::fs;

#[derive(Serialize, Deserialize, Debug)]
pub struct AspNetConfig {
    pub sdk_image: String,
    pub publish_steps: Vec<String>,
    pub final_steps: Vec<String>,
    pub asp_net_frontend_config: Option<AspNetFrontendConfig>,
}

impl AspNetConfig {
    pub fn from_json_file(file_path: &str) -> Result<Self, serde_json::Error> {
        let file_content = fs::read_to_string(file_path)
            .expect("Error reading the config file");
        serde_json::from_str(&file_content)
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub struct AspNetFrontendConfig {
    pub build_stage: String,
    pub output_directory: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct AspNetDefaults {
    pub version: String,
    pub project_name: String,
    pub csproj_file: String,
    pub project_executable: String,
    pub expose_ports: Vec<String>,
}