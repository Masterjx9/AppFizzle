// @refresh reload
import { createSignal } from "solid-js";
import "./app.css";
export default function App() {
  const [count, setCount] = createSignal(0);
  return (
    <main>
      <h1>Welcome to AppFizzle!</h1>
      <p>This is a basic Solid application.</p>
      <button class="increment" onClick={() => setCount(count() + 1)}>
        Clicks: {count()}
      </button>
      <p>
        Visit{" "}
        <a href="https://start.solidjs.com" target="_blank">
          start.solidjs.com
        </a>{" "}
        to learn how to build SolidStart apps.
      </p>
    </main>
  );
}
