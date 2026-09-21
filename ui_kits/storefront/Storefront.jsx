const { Button, ProductRow, StatusMessage } = (window.__DS || (window.__DS = Object.keys(window).filter(k=>/DesignSystem/.test(k)).map(k=>window[k]).find(o=>o&&o.Button)||{}));
const { useState } = React;

const PRODUCTS = [
  { id: "p1", title: "New Beginnings — Study Access", format: "digital", priceCents: 2400, meta: "4-week digital study" },
  { id: "p2", title: "Rooted: A Bible Study Book", format: "physical", priceCents: 1800, meta: "Paperback, ships in 3-5 days" },
  { id: "p3", title: "Rooted — Study + Book Bundle", format: "digital", priceCents: 3600, meta: "Book + web app access" },
];

function ProductCard({ p, onAdd }) {
  return (
    <div style={{ border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)", padding: 20, display: "flex", flexDirection: "column", gap: 12 }}>
      <div style={{ width: "100%", aspectRatio: "4/3", background: "var(--surface-fill)", borderRadius: "var(--radius-sm)" }} />
      <div>
        <p style={{ margin: "0 0 4px", fontWeight: 500 }}>{p.title}</p>
        <p style={{ margin: 0, fontSize: 14, color: "var(--text-secondary)" }}>{p.meta}</p>
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontWeight: 600 }}>${(p.priceCents / 100).toFixed(2)}</span>
        <button onClick={() => onAdd(p)} style={{ background: "var(--sdr-ember-500)", color: "var(--sdr-ink)", border: "none", borderRadius: 4, padding: "8px 16px", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Add to cart</button>
      </div>
    </div>
  );
}

function Header({ view, setView, cartCount }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "20px 40px", background: "var(--sdr-ink)" }}>
      <span style={{ fontFamily: "'Anton',sans-serif", textTransform: "uppercase", letterSpacing: "0.02em", fontSize: 20, cursor: "pointer", background: "linear-gradient(90deg,var(--sdr-gold-500) 0%,var(--sdr-ember-500) 55%,var(--sdr-ember-700) 100%)", WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }} onClick={() => setView("shop")}>Soul Dust Revival</span>
      <div style={{ display: "flex", gap: 16, alignItems: "center", fontSize: 14 }}>
        <a href="../../Soul Dust Revival Homepage.html" style={{ color: "#d9c3a3", textDecoration: "none" }}>Home</a>
        <a href="#" onClick={(e) => { e.preventDefault(); setView("shop"); }} style={{ color: "#d9c3a3", textDecoration: "none" }}>Shop</a>
        <a href="#" onClick={(e) => { e.preventDefault(); setView("cart"); }} style={{ color: "#d9c3a3", textDecoration: "none" }}>Cart ({cartCount})</a>
      </div>
    </div>
  );
}

function Shop({ onAdd }) {
  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: "40px 40px" }}>
      <h1 style={{ fontFamily: "'Anton',sans-serif", textTransform: "uppercase", fontSize: 32, marginBottom: 24 }}>Studies & Books</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 20 }}>
        {PRODUCTS.map((p) => <ProductCard key={p.id} p={p} onAdd={onAdd} />)}
      </div>
    </div>
  );
}

function Cart({ items, removeItem, setView }) {
  const total = items.reduce((s, i) => s + i.priceCents, 0);
  if (items.length === 0) return <div style={{ maxWidth: 576, margin: "0 auto", padding: "80px 20px", textAlign: "center", color: "var(--text-secondary)" }}>Your cart is empty.</div>;
  return (
    <div style={{ maxWidth: 576, margin: "0 auto", padding: "64px 20px", display: "flex", flexDirection: "column", gap: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Checkout</h1>
      <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 12 }}>
        {items.map((item, i) => (
          <li key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid var(--border-default)", paddingBottom: 12 }}>
            <div>
              <p style={{ margin: 0, fontWeight: 500 }}>{item.title}</p>
              <p style={{ margin: 0, fontSize: 14, color: "var(--text-secondary)" }}>Qty 1 · {item.format}</p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span>${(item.priceCents / 100).toFixed(2)}</span>
              <button onClick={() => removeItem(i)} style={{ fontSize: 14, color: "var(--text-tertiary)", background: "none", border: "none", cursor: "pointer" }}>Remove</button>
            </div>
          </li>
        ))}
      </ul>
      <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 600, fontSize: 18 }}>
        <span>Total</span><span>${(total / 100).toFixed(2)}</span>
      </div>
      <button onClick={() => setView("success")} style={{ background: "var(--sdr-ember-500)", color: "var(--sdr-ink)", border: "none", borderRadius: 4, padding: "16px 32px", fontWeight: 700, fontSize: 15, cursor: "pointer" }}>Proceed to payment</button>
    </div>
  );
}

function Success({ items, setView }) {
  const hasDigital = items.some((i) => i.format === "digital");
  const total = items.reduce((s, i) => s + i.priceCents, 0);
  return (
    <div style={{ maxWidth: 576, margin: "0 auto", padding: "64px 20px", display: "flex", flexDirection: "column", gap: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Thank you for your order</h1>
      <p style={{ margin: 0, color: "var(--text-secondary)" }}>Order #a1b2c3d4</p>
      <div style={{ borderTop: "1px solid var(--border-default)", borderBottom: "1px solid var(--border-default)", padding: "16px 0", display: "flex", flexDirection: "column", gap: 8 }}>
        {items.map((item, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between" }}><span>{item.title}</span><span>${(item.priceCents / 100).toFixed(2)}</span></div>
        ))}
        <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 600, paddingTop: 8 }}><span>Total</span><span>${(total / 100).toFixed(2)}</span></div>
      </div>
      {hasDigital ? <button onClick={() => setView("shop")} style={{ background: "var(--sdr-ember-500)", color: "var(--sdr-ink)", border: "none", borderRadius: 4, padding: "16px 32px", fontWeight: 700, fontSize: 15, cursor: "pointer" }}>Log in to access your content</button> : <p style={{ color: "var(--text-secondary)" }}>A confirmation with these details has also been sent to your email.</p>}
    </div>
  );
}

function App() {
  const [view, setView] = useState("shop");
  const [items, setItems] = useState([]);
  const addItem = (p) => setItems((it) => [...it, p]);
  const removeItem = (i) => setItems((it) => it.filter((_, idx) => idx !== i));
  return (
    <div>
      <Header view={view} setView={setView} cartCount={items.length} />
      {view === "shop" && <Shop onAdd={addItem} />}
      {view === "cart" && <Cart items={items} removeItem={removeItem} setView={setView} />}
      {view === "success" && <Success items={items} setView={setView} />}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
