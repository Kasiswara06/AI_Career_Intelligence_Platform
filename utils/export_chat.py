import os
from pathlib import Path
from typing import List, Dict, Any

def export_chat_to_txt(session_title: str, messages: List[Dict[str, Any]]) -> str:
    """Generates plain text chat transcript for export."""
    lines = [f"=== AI Career Assistant Chat Log: {session_title} ===", ""]
    for msg in messages:
        sender = "👤 User" if msg.get("question") else "🤖 AI Assistant"
        q = msg.get("question") or msg.get("message", "")
        a = msg.get("answer") or ""
        ts = msg.get("timestamp") or msg.get("created_at") or ""
        
        if q:
            lines.append(f"[{ts}] 👤 User:\n{q}\n")
        if a:
            lines.append(f"[{ts}] 🤖 AI Assistant:\n{a}\n")
        lines.append("-" * 50)

    return "\n".join(lines)

def export_chat_to_pdf(session_title: str, messages: List[Dict[str, Any]]) -> bytes:
    """Generates PDF bytes for chat session export using ReportLab or fallback plain bytes."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import io

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"<b>AI Career Assistant Chat Log: {session_title}</b>", styles['Title']))
        story.append(Spacer(1, 12))

        for msg in messages:
            q = msg.get("question", "")
            a = msg.get("answer", "")
            if q:
                story.append(Paragraph(f"<b>👤 User:</b> {q}", styles['Normal']))
                story.append(Spacer(1, 6))
            if a:
                clean_a = a.replace("\n", "<br/>").replace("*", "")
                story.append(Paragraph(f"<b>🤖 AI:</b> {clean_a[:500]}...", styles['Normal']))
                story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        # Fallback to plain bytes text format
        txt_str = export_chat_to_txt(session_title, messages)
        return txt_str.encode("utf-8")
