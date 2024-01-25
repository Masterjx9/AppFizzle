// common/mod.rs

use crate::backends::{asp_net_core, django};
use crate::frontends::angular;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct FrameworkConfig {
    pub base_image: String,
    pub workdir: String,
    pub expose_ports: Vec<String>,
    pub build_steps: Vec<String>,
    // Common fields...
}

pub enum ConfigType {
    AspNet(asp_net_core::AspNetConfig),
    Django(django::DjangoConfig),
    Angular(angular::AngularConfig),
    // Other frameworks...
}

pub fn determine_config_type(json_input: &str) -> ConfigType {
    if json_input.contains("asp_net_core") {
        ConfigType::AspNet(asp_net_core::AspNetConfig::default()) // Replace with actual parsing logic
    } else if json_input.contains("django") {
        ConfigType::Django(django::DjangoConfig::default()) // Replace with actual parsing logic
    } else {
        // Default or error handling
    }
}

