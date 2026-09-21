const { Input, Textarea, Select, Checkbox, Button, Tabs, ProductRow, StatusMessage } = (window.__DS || (window.__DS = Object.keys(window).filter(k=>/DesignSystem/.test(k)).map(k=>window[k]).find(o=>o&&o.Button)||{}));
const { useState } = React;

function Nav({ section, setSection }) {
  return (
    <div style={{ maxWidth: 896, margin: "0 auto", padding: "40px 40px 0" }}>
      <nav style={{ display: "flex", gap: 16, borderBottom: "1px solid var(--border-default)", paddingBottom: 16, marginBottom: 32 }}>
        <a href="#" onClick={(e) => { e.preventDefault(); setSection("products"); }} style={{ fontWeight: 500, color: "var(--text-link)", textDecoration: "none" }}>Products</a>
        <a href="#" onClick={(e) => { e.preventDefault(); setSection("studies"); }} style={{ fontWeight: 500, color: "var(--text-link)", textDecoration: "none" }}>Studies</a>
      </nav>
    </div>
  );
}

const PRODUCTS = [
  { id: "p1", title: "New Beginnings — Study Access", format: "digital", priceCents: 2400, active: true },
  { id: "p2", title: "Rooted: A Bible Study Book", format: "physical", priceCents: 1800, active: true },
  { id: "p3", title: "Legacy Study (2023)", format: "digital", priceCents: 1500, active: false },
];

function ProductsList({ onNew, onOpen }) {
  return (
    <div style={{ maxWidth: 896, margin: "0 auto", padding: "0 40px 60px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <h1 style={{ fontSize: 20, fontWeight: 600, margin: 0 }}>Products</h1>
        <Button size="sm" onClick={onNew}>Add product</Button>
      </div>
      <div style={{ border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)" }}>
        {PRODUCTS.map((p, i) => (
          <div key={p.id} onClick={() => onOpen(p)} style={{ borderTop: i ? "1px solid var(--border-default)" : "none", cursor: "pointer" }}>
            <ProductRow title={p.title} meta={`${p.format} · $${(p.priceCents / 100).toFixed(2)}${!p.active ? " · inactive" : ""}`} />
          </div>
        ))}
      </div>
    </div>
  );
}

function ProductForm({ product, onDone }) {
  const [title, setTitle] = useState(product?.title ?? "");
  const [format, setFormat] = useState(product?.format ?? "digital");
  const [active, setActive] = useState(product?.active ?? true);
  return (
    <div style={{ maxWidth: 512, margin: "0 auto", padding: "0 40px 60px" }}>
      <h1 style={{ fontSize: 20, fontWeight: 600, marginBottom: 20 }}>{product ? "Edit product" : "Add product"}</h1>
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <Input label="Title" id="pt" required value={title} onChange={(e) => setTitle(e.target.value)} />
        <Textarea label="Description" id="pd" rows={4} value="" onChange={() => {}} />
        <div style={{ display: "flex", gap: 16 }}>
          <Input label="Price (USD)" id="pp" type="number" value="24.00" onChange={() => {}} />
          <Select label="Format" id="pf" value={format} onChange={(e) => setFormat(e.target.value)} options={[{ value: "physical", label: "Physical (ships)" }, { value: "digital", label: "Digital / web app access" }]} />
        </div>
        <Checkbox id="pa" label="Active (visible for purchase)" checked={active} onChange={(e) => setActive(e.target.checked)} />
        <div><Button onClick={onDone}>Save product</Button></div>
      </div>
    </div>
  );
}

const STUDIES = [
  { id: "st1", title: "New Beginnings", published: true },
  { id: "st2", title: "Rooted", published: false },
];

function StudiesList({ onNew, onOpen }) {
  return (
    <div style={{ maxWidth: 896, margin: "0 auto", padding: "0 40px 60px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <h1 style={{ fontSize: 20, fontWeight: 600, margin: 0 }}>Studies</h1>
        <Button size="sm" onClick={onNew}>New study</Button>
      </div>
      <div style={{ border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)" }}>
        {STUDIES.map((s, i) => (
          <div key={s.id} onClick={() => onOpen(s)} style={{ borderTop: i ? "1px solid var(--border-default)" : "none", padding: 16, display: "flex", justifyContent: "space-between", cursor: "pointer" }}>
            <span>{s.title}</span><span style={{ fontSize: 14, color: "var(--text-tertiary)" }}>{!s.published && "draft"}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function NewStudy({ onDone }) {
  const [tab, setTab] = useState("manual");
  return (
    <div style={{ maxWidth: 512, margin: "0 auto", padding: "0 40px 60px" }}>
      <h1 style={{ fontSize: 20, fontWeight: 600, marginBottom: 20 }}>New study</h1>
      <Tabs tabs={[{ value: "manual", label: "Create manually" }, { value: "import", label: "Import from document" }]} active={tab} onChange={setTab} />
      <div style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 20 }}>
        {tab === "manual" ? (
          <React.Fragment>
            <Input label="Title" id="st" required value="" onChange={() => {}} />
            <Input label="Slug (URL path)" id="ss" required value="" onChange={() => {}} />
            <div><Button onClick={onDone}>Save study</Button></div>
          </React.Fragment>
        ) : (
          <React.Fragment>
            <div>
              <label style={{ display: "block", fontSize: 14, fontWeight: 500, marginBottom: 4 }}>Document (.docx or .pdf)</label>
              <input type="file" />
              <p style={{ fontSize: 12, color: "var(--text-tertiary)", marginTop: 4 }}>.docx files split into lessons using the document's own heading styles (most reliable). .pdf files split using a "Week 1 / Lesson 2" heuristic.</p>
            </div>
            <div><Button onClick={onDone}>Import document</Button></div>
          </React.Fragment>
        )}
      </div>
    </div>
  );
}

const BLOCK_TYPES = [
  { type: "text", label: "Text" },
  { type: "callout", label: "Callout / color block" },
  { type: "question", label: "Question" },
  { type: "video", label: "Video" },
];

function BlockEditor({ block, onDelete }) {
  return (
    <div style={{ border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)", padding: 16, background: "var(--surface-page)", display: "flex", flexDirection: "column", gap: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <span style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-tertiary)" }}>{block.type}</span>
        <button onClick={onDelete} style={{ fontSize: 13, color: "var(--state-error-strong)", background: "none", border: "none", cursor: "pointer" }}>Delete</button>
      </div>
      {block.type === "text" && <Textarea id={`b-${block.id}`} rows={3} value="Every study begins somewhere..." onChange={() => {}} />}
      {block.type === "callout" && (
        <React.Fragment>
          <Input id={`bt-${block.id}`} value="Key Verse" onChange={() => {}} />
          <Textarea id={`bb-${block.id}`} rows={2} value='"Behold, I am doing a new thing..."' onChange={() => {}} />
        </React.Fragment>
      )}
      {block.type === "question" && <Textarea id={`bq-${block.id}`} rows={2} value="What is one area where you're waiting to see something new?" onChange={() => {}} />}
      {block.type === "video" && <React.Fragment><input type="file" accept="video/*" /><StatusMessage tone="warning">Captions are required for video content (WCAG 1.2.2).</StatusMessage></React.Fragment>}
    </div>
  );
}

function SortableItem({ block, index, total, onMove, onDelete }) {
  return (
    <div style={{ display: "flex", gap: 8 }}>
      <div style={{ cursor: "grab", paddingTop: 16, color: "var(--text-tertiary)", userSelect: "none" }} aria-label="Drag to reorder">⠿</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 4, paddingTop: 16 }}>
        <button onClick={() => onMove(index, "up")} disabled={index === 0} style={{ fontSize: 11, border: "1px solid var(--border-default)", borderRadius: 4, padding: "2px 6px", opacity: index === 0 ? 0.3 : 1, background: "none", cursor: "pointer" }}>↑</button>
        <button onClick={() => onMove(index, "down")} disabled={index === total - 1} style={{ fontSize: 11, border: "1px solid var(--border-default)", borderRadius: 4, padding: "2px 6px", opacity: index === total - 1 ? 0.3 : 1, background: "none", cursor: "pointer" }}>↓</button>
      </div>
      <div style={{ flex: 1 }}><BlockEditor block={block} onDelete={() => onDelete(index)} /></div>
    </div>
  );
}

function LessonEditor({ onBack }) {
  const [blocks, setBlocks] = useState([{ id: 1, type: "text" }, { id: 2, type: "callout" }, { id: 3, type: "question" }]);
  const [menuOpen, setMenuOpen] = useState(false);
  function move(index, dir) {
    const j = dir === "up" ? index - 1 : index + 1;
    if (j < 0 || j >= blocks.length) return;
    const copy = [...blocks]; [copy[index], copy[j]] = [copy[j], copy[index]]; setBlocks(copy);
  }
  function del(index) { setBlocks(blocks.filter((_, i) => i !== index)); }
  function add(type) { setBlocks([...blocks, { id: Date.now(), type }]); setMenuOpen(false); }
  return (
    <div style={{ maxWidth: 672, margin: "0 auto", padding: "0 40px 60px" }}>
      <button onClick={onBack} style={{ background: "none", border: "none", color: "var(--text-secondary)", fontSize: 14, cursor: "pointer", padding: 0, marginBottom: 16 }}>← Back to lessons</button>
      <h1 style={{ fontSize: 20, fontWeight: 600, marginBottom: 20 }}>Lesson 1: A New Thing</h1>
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {blocks.map((b, i) => <SortableItem key={b.id} block={b} index={i} total={blocks.length} onMove={move} onDelete={del} />)}
      </div>
      <div style={{ position: "relative", marginTop: 16 }}>
        <button onClick={() => setMenuOpen((o) => !o)} style={{ border: "1px dashed var(--border-default)", borderRadius: "var(--radius-md)", padding: "12px 16px", width: "100%", color: "var(--text-secondary)", background: "none", cursor: "pointer" }}>+ Add block</button>
        {menuOpen && (
          <div style={{ position: "absolute", background: "#fff", border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)", boxShadow: "var(--shadow-popover)", marginTop: 4, width: 224 }}>
            {BLOCK_TYPES.map((t) => <button key={t.type} onClick={() => add(t.type)} style={{ display: "block", width: "100%", textAlign: "left", padding: "8px 16px", background: "none", border: "none", cursor: "pointer" }}>{t.label}</button>)}
          </div>
        )}
      </div>
    </div>
  );
}

function StudyDetail({ study, onBack, onOpenLesson }) {
  const lessons = [{ id: "l1", title: "Lesson 1: A New Thing", published: true }, { id: "l2", title: "Lesson 2: Letting Go", published: false }];
  return (
    <div style={{ maxWidth: 896, margin: "0 auto", padding: "0 40px 60px" }}>
      <button onClick={onBack} style={{ background: "none", border: "none", color: "var(--text-secondary)", fontSize: 14, cursor: "pointer", padding: 0, marginBottom: 16 }}>← Studies</button>
      <h1 style={{ fontSize: 20, fontWeight: 600, marginBottom: 20 }}>Edit study — {study.title}</h1>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, margin: 0 }}>Lessons</h2>
        <Button size="sm">New lesson</Button>
      </div>
      <div style={{ border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)" }}>
        {lessons.map((l, i) => (
          <div key={l.id} onClick={() => onOpenLesson(l)} style={{ borderTop: i ? "1px solid var(--border-default)" : "none", padding: 16, display: "flex", justifyContent: "space-between", cursor: "pointer" }}>
            <span>{l.title}</span><span style={{ fontSize: 14, color: "var(--text-tertiary)" }}>{!l.published && "draft"}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  const [section, setSection] = useState("products");
  const [screen, setScreen] = useState({ name: "list" });

  if (section === "products") {
    if (screen.name === "form") return <React.Fragment><Nav section={section} setSection={(s) => { setSection(s); setScreen({ name: "list" }); }} /><ProductForm product={screen.product} onDone={() => setScreen({ name: "list" })} /></React.Fragment>;
    return <React.Fragment><Nav section={section} setSection={(s) => { setSection(s); setScreen({ name: "list" }); }} /><ProductsList onNew={() => setScreen({ name: "form" })} onOpen={(p) => setScreen({ name: "form", product: p })} /></React.Fragment>;
  }
  if (screen.name === "new") return <React.Fragment><Nav section={section} setSection={(s) => { setSection(s); setScreen({ name: "list" }); }} /><NewStudy onDone={() => setScreen({ name: "list" })} /></React.Fragment>;
  if (screen.name === "detail") return <React.Fragment><Nav section={section} setSection={(s) => { setSection(s); setScreen({ name: "list" }); }} /><StudyDetail study={screen.study} onBack={() => setScreen({ name: "list" })} onOpenLesson={() => setScreen({ name: "lesson" })} /></React.Fragment>;
  if (screen.name === "lesson") return <React.Fragment><Nav section={section} setSection={(s) => { setSection(s); setScreen({ name: "list" }); }} /><LessonEditor onBack={() => setScreen({ name: "detail", study: { title: "New Beginnings" } })} /></React.Fragment>;
  return <React.Fragment><Nav section={section} setSection={(s) => { setSection(s); setScreen({ name: "list" }); }} /><StudiesList onNew={() => setScreen({ name: "new" })} onOpen={(s) => setScreen({ name: "detail", study: s })} /></React.Fragment>;
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
