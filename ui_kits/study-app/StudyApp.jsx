const { Input, Button, Textarea, ProgressBar, Callout, StatusMessage } = (window.__DS || (window.__DS = Object.keys(window).filter(k=>/DesignSystem/.test(k)).map(k=>window[k]).find(o=>o&&o.Button)||{}));
const { useState, useEffect, useRef } = React;

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const ref = useRef(null);
  useEffect(() => { if (sent) ref.current?.focus(); }, [sent]);
  if (sent) return (
    <div style={{ maxWidth: 384, margin: "0 auto", padding: "80px 20px", textAlign: "center" }}>
      <p ref={ref} tabIndex={-1} role="status">Check your email for a login link.</p>
      <button onClick={() => onLogin()} style={{ marginTop: 16, background: "none", border: "none", color: "var(--text-tertiary)", fontSize: 13, cursor: "pointer" }}>(demo: skip to app →)</button>
    </div>
  );
  return (
    <form onSubmit={(e) => { e.preventDefault(); setSent(true); }} style={{ maxWidth: 384, margin: "0 auto", padding: "80px 20px", display: "flex", flexDirection: "column", gap: 16 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600, margin: 0 }}>Log in</h1>
      <Input id="email" type="email" required placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />
      <Button type="submit">Send login link</Button>
    </form>
  );
}

const STUDIES = [
  { id: "s1", title: "New Beginnings", desc: "A 4-week study on starting again.", progress: 2, total: 4 },
  { id: "s2", title: "Rooted", desc: "A 6-week study on staying grounded.", progress: 0, total: 6 },
];

function StudiesIndex({ onOpen }) {
  return (
    <div style={{ maxWidth: 672, margin: "0 auto", padding: "48px 20px", display: "flex", flexDirection: "column", gap: 20 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Your studies</h1>
      {STUDIES.map((s) => (
        <div key={s.id} onClick={() => onOpen(s)} style={{ border: "1px solid var(--border-default)", borderRadius: "var(--radius-md)", padding: 20, cursor: "pointer", display: "flex", flexDirection: "column", gap: 10 }}>
          <p style={{ margin: 0, fontWeight: 600, fontSize: 18 }}>{s.title}</p>
          <p style={{ margin: 0, color: "var(--text-secondary)", fontSize: 14 }}>{s.desc}</p>
          <ProgressBar completed={s.progress} total={s.total} />
          <p style={{ margin: 0, fontSize: 12, color: "var(--text-tertiary)" }}>{s.progress} of {s.total} lessons complete</p>
        </div>
      ))}
    </div>
  );
}

function QuestionBlock() {
  const [answer, setAnswer] = useState("");
  const [saved, setSaved] = useState(false);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <label style={{ fontWeight: 500 }}>What is one area where you're waiting to see something new take root?</label>
      <Textarea rows={4} value={answer} onChange={(e) => { setAnswer(e.target.value); setSaved(false); }} />
      <div onBlur={() => setSaved(true)} tabIndex={-1}><Button size="sm" onClick={() => setSaved(true)}>Save answer</Button></div>
      <StatusMessage tone="muted">{saved ? "Saved" : ""}</StatusMessage>
    </div>
  );
}

function LessonView({ study, onBack }) {
  return (
    <div style={{ maxWidth: 672, margin: "0 auto", padding: "40px 20px", display: "flex", flexDirection: "column", gap: 24 }}>
      <button onClick={onBack} style={{ alignSelf: "flex-start", background: "none", border: "none", color: "var(--text-secondary)", fontSize: 14, cursor: "pointer", padding: 0 }}>← {study.title}</button>
      <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Lesson 1: A New Thing</h1>
      <p style={{ margin: 0, lineHeight: 1.6 }}>Every study begins somewhere. This lesson opens with a short reading on what it means to start again, drawing on the idea of new beginnings as an active, ongoing choice rather than a single moment.</p>

      <div style={{ aspectRatio: "16/9", background: "var(--surface-fill)", borderRadius: "var(--radius-md)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-tertiary)", fontSize: 14 }}>Video player (captions required)</div>
      <details><summary style={{ cursor: "pointer", fontSize: 14, fontWeight: 500 }}>View transcript</summary><p style={{ marginTop: 8, fontSize: 14, color: "var(--text-secondary)", whiteSpace: "pre-wrap" }}>Full text transcript of the video appears here for screen-reader and no-media access.</p></details>

      <div style={{ display: "flex", alignItems: "center", gap: 12, background: "var(--surface-sunken)", borderRadius: "var(--radius-md)", padding: "12px 16px" }}>
        <span style={{ fontSize: 13, color: "var(--text-secondary)" }}>Audio companion</span>
        <div style={{ flex: 1, height: 4, background: "var(--surface-fill)", borderRadius: 999 }} />
      </div>

      <Callout title="Key Verse" color="#fef3c7"><p style={{ margin: 0 }}>"Behold, I am doing a new thing; now it springs forth, do you not perceive it?"</p></Callout>

      <QuestionBlock />

      <Callout title="Prayer Prompt" color="#dcfce7"><p style={{ margin: 0 }}>Close this lesson with a short prayer of your own, using today's reading as a starting point.</p></Callout>
    </div>
  );
}

function App() {
  const [screen, setScreen] = useState("login");
  const [study, setStudy] = useState(null);
  if (screen === "login") return <Login onLogin={() => setScreen("index")} />;
  if (screen === "index") return <StudiesIndex onOpen={(s) => { setStudy(s); setScreen("lesson"); }} />;
  return <LessonView study={study} onBack={() => setScreen("index")} />;
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
