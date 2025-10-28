import React, { useState } from "react";
import "./App.css";

// Helper function to render the review text with styled labels
const renderReviewText = (review) => {
  const match = review.match(/^(.*) ➝ \[(Fake|Real)\]$/);
  if (match) {
    const text = match[1];
    const label = match[2];
    const labelClass = label.toLowerCase() === 'fake' ? 'fake-label' : 'real-label';

    return (
      <>
        {text}{' '}
        <span style={{ fontWeight: 400, color: '#6c757d' }}>➝</span>{' '}
        <span className={labelClass} style={{ marginLeft: '5px' }}>
            [{label}]
        </span>
      </>
    );
  }
  return review;
};

function App() {
  const products = [
    {
      id: 1,
      name: "Wireless Headphones",
      price: 1999,
      image: "https://m.media-amazon.com/images/I/51FNnHjzhQL._UF1000,1000_QL80_.jpg",
    },
    {
      id: 2,
      name: "Smartphone",
      price: 14999,
      image: "https://platform.theverge.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/25626687/DSC08433.jpg?quality=90&strip=all&crop=16.675%2C0%2C66.65%2C100&w=2400",
    },
    {
      id: 3,
      name: "Coffee Maker",
      price: 2499,
      image: "https://m.media-amazon.com/images/I/61x2BKrHBKL._UF894,1000_QL80_.jpg",
    },
    {
      id: 4,
      name: "Laptop",
      price: 49999,
      image: "https://m.media-amazon.com/images/I/510uTHyDqGL.jpg",
    },
    {
      id: 5,
      name: "Smartwatch",
      price: 7999,
      image: "https://m.media-amazon.com/images/I/71nzWfUAt+L._UF1000,1000_QL80_.jpg",
    },
    {
      id: 6,
      name: "Gaming Chair",
      price: 11999,
      image: "https://drogo.in/cdn/shop/files/DGC003.jpg?v=1749299158",
    },
    {
      id: 7,
      name: "Air Conditioner",
      price: 29999,
      image: "https://api.hisense-india.com/media/categories/air-conditioner-thumb_image-1675223163-6794.png",
    },
    {
      id: 8,
      name: "Bluetooth Speaker",
      price: 2999,
      image: "https://m.media-amazon.com/images/I/71L9o0-0SML._UF1000,1000_QL80_.jpg",
    },
  ];
  
  const [reviews, setReviews] = useState({});
  // NEW: State to hold input text for EACH product, keyed by productId
  const [inputReviewTexts, setInputReviewTexts] = useState({}); 
  const [loading, setLoading] = useState(false);

  // Handler to update the input state for a specific product ID
  const handleInputChange = (productId, value) => {
    setInputReviewTexts(prev => ({
      ...prev,
      [productId]: value
    }));
  };

  const handleReviewSubmit = async (productId) => {
    // Get the specific review text for this product
    const reviewText = inputReviewTexts[productId] || ""; 
    if (!reviewText.trim()) return;

    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ review: reviewText }),
      });

      const data = await response.json();
      const label = data.prediction; 

      setReviews((prev) => ({
        ...prev,
        [productId]: [
          ...(prev[productId] || []),
          `${reviewText} ➝ [${label}]`, 
        ],
      }));
      
      // Clear the input text ONLY for the submitted product
      handleInputChange(productId, ""); 

    } catch (error) {
      console.error("Error connecting to backend:", error);
      alert(
        "Failed to reach backend. Make sure Flask server is running on http://localhost:5000"
      );
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="navbar-brand">Best Buy</div>
        <div className="navbar-links">
          <a href="#">Home</a>
          <a href="#">Categories</a>
          <a href="#">Cart</a>
          <a href="#">Contact</a>
        </div>
      </nav>

      <h1 className="store-title">Welcome to Best Buy</h1>

      <div className="product-list">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            <img
              src={product.image}
              alt={product.name}
              className="product-image"
            />
            <h2>{product.name}</h2>
            <p className="price">₹{product.price}</p>

            <h3>Customer Reviews</h3>
            <ul className="review-list">
              {(reviews[product.id] || []).map((rev, idx) => (
                <li key={idx}>
                  {renderReviewText(rev)} 
                </li>
              ))}
            </ul>

            <input
              type="text"
              placeholder="Write a review..."
              // Binds to the specific product's text
              value={inputReviewTexts[product.id] || ""} 
              // Updates ONLY the specific product's state
              onChange={(e) => handleInputChange(product.id, e.target.value)}
              className="review-input"
            />
            <button
              onClick={() => handleReviewSubmit(product.id)}
              className="submit-button"
              disabled={loading}
            >
              {loading ? "Checking..." : "Submit Review"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;