// assets/js/button_click_controller.js
import { Controller } from "@hotwired/stimulus";

export default class ButtonClickController extends Controller {
  connect() {
    this.element.addEventListener('click', () => {
      alert('Hello from AppFizzle!');
    });
  }
}
