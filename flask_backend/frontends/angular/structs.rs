// Module: structs
use serde::{Serialize, Deserialize};
use serde_json;


#[derive(Serialize, Deserialize, Debug)]
pub struct AngularConfig {
    pub base_image: String,
    pub build_steps: Vec<String>,
    pub output_directory: String,
    pub defaults: AngularDefaults,
}

impl AngularConfig {
    pub fn from_json_file(file_path: &str) -> Result<Self, serde_json::Error> {
        let file_content = std::fs::read_to_string(file_path)
            .expect("Error reading the config file");
        serde_json::from_str(&file_content)
    }
    
}
#[derive(Serialize, Deserialize, Debug)]
pub struct AngularDefaults {
    pub angular_app_dir: String,
    pub angular_output_dir: String,
}
