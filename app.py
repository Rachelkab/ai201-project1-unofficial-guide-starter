import gradio as gr
from query import ask

# ── Handler function ────────────────────────────────────────
def handle_query(question):
    """Takes user question, returns answer and sources."""
    
    if not question.strip():
        return "Please enter a question.", "No sources."
    
    result = ask(question)
    
    # Format sources as bullet points
    sources = "\n".join(f"• {s}" for s in result["sources"])
    
    return result["answer"], sources

# ── Build Gradio UI ─────────────────────────────────────────
with gr.Blocks(title="Utah CS Professor Guide") as demo:
    
    gr.Markdown("# 🎓 The Unofficial Utah CS Professor Guide")
    gr.Markdown("Ask questions about CS professors at SUU, University of Utah, BYU, and Utah State.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. Is Erin Parker a tough grader?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(
            label="Answer",
            lines=8
        )
        sources = gr.Textbox(
            label="Sources",
            lines=8
        )
    
    # Connect button and enter key to handler
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

# ── Launch ──────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch()