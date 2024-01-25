use serde::{Serialize, Deserialize};
use serde_json;


#[derive(Serialize, Deserialize, Debug)]
pub struct DjangoConfig {
    pub system_dependencies: Vec<String>,
}

impl DjangoConfig {
    pub fn from_json_file(file_path: &str) -> Result<Self, serde_json::Error> {
        let file_content = std::fs::read_to_string(file_path)
            .expect("Error reading the config file");
        serde_json::from_str(&file_content)
    }
    
}