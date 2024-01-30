import './App.css';
import logo from './logo.svg';

function App() {
  // Function to handle button click
  const handleClick = () => {
    alert('Hello from AppFizzle!');
  };

  return (
    <div className="App">
      <header className="App-header">
      <img src={logo} className="App-logo" alt="logo" />

        <h1>Welcome to AppFizzle!</h1>
        <p>This is a basic React application.</p>
        {/* Button with click event handler */}
        <button id="clickMeBtn" onClick={handleClick}>Click Me</button>
      </header>
    </div>
  );
}

export default App;
