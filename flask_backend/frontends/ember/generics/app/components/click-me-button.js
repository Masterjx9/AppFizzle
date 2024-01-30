import Component from '@glimmer/component';
import { action } from '@ember/object';

export default class ClickMeButtonComponent extends Component {
  @action
  showAlert() {
    alert('Hello from AppFizzle!');
  }
}
