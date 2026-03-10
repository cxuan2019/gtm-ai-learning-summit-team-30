import ImageGenerator from "./components/ImageGenerator";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Summit Athletics</h1>
        <p className="subtitle">Personalized Ad Generation</p>
      </header>
      <main>
        <ImageGenerator />
      </main>
    </div>
  );
}

export default App;
