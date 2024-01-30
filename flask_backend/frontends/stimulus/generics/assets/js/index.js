// assets/js/index.js
import { Application } from "@hotwired/stimulus";
import ButtonClickController from "./button_click_controller";

const application = Application.start();
application.register("button-click", ButtonClickController);
