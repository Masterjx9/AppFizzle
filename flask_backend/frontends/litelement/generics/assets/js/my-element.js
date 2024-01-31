import { LitElement, html, css } from 'lit';

class MyElement extends LitElement {
  static styles = css`
    button {
      padding: 10px 20px;
      font-size: 16px;
      cursor: pointer;
    }
  `;

  render() {
    return html`
      <button @click="${this.handleClick}"><slot></slot></button>
    `;
  }

  handleClick() {
    alert('Hello from AppFizzle!');
  }
}

customElements.define('my-element', MyElement);
