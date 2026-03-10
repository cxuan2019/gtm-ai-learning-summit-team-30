import { useEffect, useState } from "react";

interface Customer {
  id: string;
  name: string;
}

interface Product {
  id: string;
  title: string;
  style: string;
}

interface GenerateResult {
  summary: string;
  image_base64: string | null;
  mime_type: string;
}

function ImageGenerator() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState("");
  const [selectedProduct, setSelectedProduct] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/customers")
      .then((r) => r.json())
      .then(setCustomers);
    fetch("/api/products")
      .then((r) => r.json())
      .then(setProducts);
  }, []);

  const handleGenerate = async () => {
    if (!selectedCustomer || !selectedProduct) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: selectedCustomer,
          product_id: selectedProduct,
        }),
      });
      if (!resp.ok) throw new Error(`Server error: ${resp.status}`);
      const data: GenerateResult = await resp.json();
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator-panel">
      <div className="controls">
        <div className="control-group">
          <label htmlFor="customer-select">Customer</label>
          <select
            id="customer-select"
            value={selectedCustomer}
            onChange={(e) => setSelectedCustomer(e.target.value)}
          >
            <option value="">Select a customer...</option>
            {customers.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="product-select">Product</label>
          <select
            id="product-select"
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
          >
            <option value="">Select a product...</option>
            {products.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        className="generate-btn"
        onClick={handleGenerate}
        disabled={!selectedCustomer || !selectedProduct || loading}
      >
        {loading ? "Generating..." : "Generate Lifestyle Image"}
      </button>

      {loading && (
        <div className="loading">
          Generating your personalized ad image... This may take a moment.
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          {result.image_base64 && (
            <img
              src={`data:${result.mime_type};base64,${result.image_base64}`}
              alt="Generated lifestyle ad"
            />
          )}
          {result.summary && <div className="summary">{result.summary}</div>}
        </div>
      )}
    </div>
  );
}

export default ImageGenerator;
