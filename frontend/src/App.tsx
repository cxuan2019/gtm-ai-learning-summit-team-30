import { useEffect, useState } from "react";
import ImageGenerator from "./components/ImageGenerator";

interface Brand {
  brand_name: string;
  slogan: string;
  color: string;
  font: string;
  logo_url: string;
}

function App() {
  const [brand, setBrand] = useState<Brand | null>(null);

  useEffect(() => {
    fetch("/api/brand")
      .then((r) => r.json())
      .then(setBrand);
  }, []);

  return (
    <div className="app">
      <header
        className="app-header"
        style={brand ? { background: brand.color } : undefined}
      >
        <div className="header-content">
          {brand?.logo_url && (
            <img src={brand.logo_url} alt={brand.brand_name} className="brand-logo" />
          )}
          <div>
            <h1>{brand?.brand_name ?? "Loading..."}</h1>
            <p className="subtitle">Personalized Ad Generation</p>
            {brand?.slogan && <p className="slogan">{brand.slogan}</p>}
          </div>
        </div>
      </header>
      <main>
        <ImageGenerator />
      </main>
    </div>
  );
}

export default App;
