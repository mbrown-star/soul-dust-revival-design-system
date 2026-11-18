"""
guards.py -- the hard checks the cover scripts share, so a bad build stops with an error
instead of shipping. Standard library only. These run inside the scripts themselves, so
they apply everywhere the pipeline runs (Claude Code, Cowork, a plain terminal), not only
where Claude Code hooks fire.

  - build_dir():          build/ beside the scripts, or $SDR_COVER_BUILD (the Claude Code
                          hooks build into a scratch folder so they never touch yours).
  - pdf_page_count():     page count of an interior PDF, for the spine-width check in to_pdf.py.
  - stamp_path()/sha256(): verify_covers.py stamps each PNG it passed; to_pdf.py exports only
                          a PNG whose hash matches its stamp.
  - register_grounds():   (title, hex) rows from the README's register, for gen_covers.py's
                          duplicate-ground check.
  - find_footer_keys():   any "footer" field in a copy file (the 2026-10-02 directive).
"""
import hashlib
import os
import re
import zlib


class GuardError(SystemExit):
    """Raised to stop a script with a clear message and a non-zero exit."""

    def __init__(self, msg):
        super().__init__("REFUSED: " + msg)


def build_dir(base):
    return os.path.abspath(os.environ.get("SDR_COVER_BUILD") or os.path.join(base, "build"))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stamp_path(build, key):
    return os.path.join(build, ".verified-" + key)


# ---- PDF page count (no third-party PDF library) ----
_PAGES_OBJ = re.compile(rb"/Type\s*/Pages\b")
_COUNT = re.compile(rb"/Count\s+(\d+)")
_STREAM = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)


def _counts_in(blob):
    """/Count values of every /Type /Pages dictionary in blob."""
    out = []
    for mo in _PAGES_OBJ.finditer(blob):
        # The dictionary around this /Type: back to its opening "<<", forward to its closing ">>".
        start = blob.rfind(b"<<", 0, mo.start())
        end = blob.find(b">>", mo.end())
        if start < 0 or end < 0:
            continue
        # Kids arrays may contain nested << >> in odd files; widen to the object end if needed.
        obj_end = blob.find(b"endobj", mo.end())
        seg = blob[start:obj_end if obj_end > 0 else end + 2]
        c = _COUNT.search(seg)
        if c:
            out.append(int(c.group(1)))
    return out


def pdf_page_count(path):
    """Pages in a PDF: the largest /Count of any /Pages node (the root's), searching plain
    objects and FlateDecode object streams. Raises GuardError if it can't be read."""
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(b"%PDF"):
        raise GuardError(f"{path} is not a PDF")
    counts = _counts_in(data)
    for mo in _STREAM.finditer(data):
        try:
            counts += _counts_in(zlib.decompress(mo.group(1)))
        except zlib.error:
            pass
    if not counts:
        raise GuardError(f"could not read a page count from {path}")
    return max(counts)


# ---- README register ----
_HEX = re.compile(r"#[0-9a-fA-F]{6}\b")


def register_grounds(readme_path):
    """[(title, '#rrggbb')] from the 'Register of shipped covers' table in the README."""
    rows, in_reg = [], False
    with open(readme_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                in_reg = line.strip().lower().startswith("## register")
                continue
            if not in_reg or not line.startswith("|") or line.startswith("|---"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 6 or cells[0] == "Title":
                continue
            hexes = _HEX.findall(cells[-1])
            if hexes:
                rows.append((cells[0], hexes[-1].lower()))
    return rows


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def register_rows_for(title, rows):
    """Register rows that belong to this copy file's title. A row belongs to it when the row's
    title is the copy file's title or starts with it ("John" owns every "John: ... Part N" row,
    which share one ground on purpose)."""
    t = _norm(title)
    return [r for r in rows if _norm(r[0]) == t or _norm(r[0]).startswith(t + " ")]


def find_footer_keys(obj, path=""):
    """Every key containing 'footer' anywhere in a copy file, as dotted paths."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if "footer" in k.lower():
                found.append(p)
            found += find_footer_keys(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += find_footer_keys(v, f"{path}[{i}]")
    return found
