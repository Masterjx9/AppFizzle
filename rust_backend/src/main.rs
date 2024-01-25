// mod backends {
//     pub mod asp_net_core;
//     pub mod django;
// }

// mod frontends {
//     pub mod angular;
// }

use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;
use serde::Serialize;
use serde_json::json;
use backends::asp_net_core::structs::AspNetConfig;
use backends::django::structs::DjangoConfig;
use frontends::angular::structs::AngularConfig;
use frontends::angular::structs::AngularDefaults;

#[derive(Debug, Deserialize)]
struct WebData {
    backend: String,
    frontend: String,
    options: Option<Vec<serde_json::Value>>,
}

async fn post_handler(web_data: web::Json<WebData>) -> impl Responder {
    println!("Received: {:?}", web_data);
    
    let json_input = match &web_data.options {
        Some(options) => options.to_string(),
        None => "".to_string(),
    };

    let config_type = determine_config_type(&json_input);

    match config_type {
        ConfigType::AspNet(asp_config) => {
            // Process ASP.NET config
            // ...
        },
        ConfigType::Django(django_config) => {
            // Process Django config
            // ...
        },
        ConfigType::Angular(angular_config) => {
            // Process Angular config
            // ...
        },
        // Handle other frameworks...
    }


    HttpResponse::Ok().json(json!({"Result": "Success"}))
}

// For testing purposes
async fn hello_world() -> impl Responder {
    HttpResponse::Ok().body("Hello World!")
}

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/builder", web::post().to(post_handler))
            .route("/", web::get().to(hello_world))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
