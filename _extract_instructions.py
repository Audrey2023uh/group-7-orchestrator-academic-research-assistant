from pathlib import Path
from pypdf import PdfReader

instr = Path(r"C:\Users\audre\OneDrive\0-1- Urgent\1- Multi_Agent_Failure_Modes_Guardrails\Instructiones")
out = Path(r"C:\Users\audre\OneDrive\0-1- Urgent\1- Multi_Agent_Failure_Modes_Guardrails\_instruction_extracts")
out.mkdir(exist_ok=True)

for pdf in sorted(instr.glob("*.pdf")):
    reader = PdfReader(str(pdf))
    parts = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        parts.append(f"\n--- PAGE {i}/{len(reader.pages)} ---\n{text}")
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in pdf.stem)[:90]
    dest = out / f"{safe}.txt"
    dest.write_text("\n".join(parts), encoding="utf-8", errors="replace")
    print(f"{pdf.name}: {len(reader.pages)} pages -> {dest.name} ({dest.stat().st_size} bytes)")
print("DONE")
