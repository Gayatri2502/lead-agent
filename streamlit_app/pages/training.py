"""AI Training: dataset preview, training runs, metrics and confusion matrix."""
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .. import state, theme
from ..ml.datasets import build_dataset
from ..ml.train import load_model, train_receptionist


def _confusion_fig(meta: Dict[str, Any]) -> go.Figure:
    intents = meta.get("intents", [])
    matrix = meta.get("confusion_matrix", [])
    fig = go.Figure(go.Heatmap(
        z=matrix, x=intents, y=intents, colorscale="Blues",
        text=matrix, texttemplate="%{text}", hovertemplate="true: %{y}<br>pred: %{x}<br>n=%{z}"))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=420,
                      paper_bgcolor="white",
                      xaxis=dict(tickangle=35, title="Predicted"),
                      yaxis=dict(title="Actual", autorange="reversed"))
    return fig


def render(cfg: Dict[str, Any]) -> None:
    theme.page_header("AI Training",
                      "The receptionist model is trained from your agent profile — "
                      "services, role vocabulary and knowledge base.")

    trainings: List[Dict[str, Any]] = state.load_trainings()
    latest = trainings[0] if trainings else None
    bundle = load_model(state.current_user()["uid"])

    # ---- status row -------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        theme.metric_card("Model status", "Trained" if bundle else "Not trained",
                          latest.get("version", "—") if latest else "run first training")
    with c2:
        theme.metric_card("Intent accuracy", f"{latest['accuracy']:.1f}%" if latest else "—",
                          "holdout test set")
    with c3:
        theme.metric_card("Macro F1", f"{latest['macro_f1']:.1f}%" if latest else "—",
                          f"{len(latest.get('intents', []))} intents" if latest else "")
    with c4:
        theme.metric_card("Training samples", latest.get("samples", "—") if latest else "—",
                          f"in {latest.get('duration_sec', '—')}s" if latest else "")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    cols = st.columns([2, 1])
    with cols[1]:
        with st.container(border=True):
            st.markdown("**Train from current profile**")
            st.caption(
                "Rebuilds the caller-intent dataset from your services, role vocabulary and "
                "knowledge base, then retrains the classifier used by the receptionist.")
            if st.button("🔁  Retrain receptionist", type="primary", use_container_width=True):
                with st.status("Training…", expanded=True) as status:
                    st.write("Generating dataset from agent profile…")
                    meta = train_receptionist(cfg, state.current_user()["uid"])
                    st.write(f"Trained on {meta['samples']} samples in {meta['duration_sec']}s")
                    st.write("Uploading training report to Firebase…")
                    state.insert("trainings", meta)
                    status.update(label=f"Done — {meta['accuracy']}% accuracy", state="complete")
                st.rerun()

    with cols[0]:
        with st.container(border=True):
            st.markdown("**Live dataset preview**")
            samples = build_dataset(cfg)
            breakdown: Dict[str, int] = {}
            for _, intent in samples:
                breakdown[intent] = breakdown.get(intent, 0) + 1
            frame = pd.DataFrame({"Intent": list(breakdown), "Samples": list(breakdown.values())})
            frame = frame.sort_values("Samples")
            fig = px.bar(frame, x="Samples", y="Intent", orientation="h")
            fig.update_traces(marker_color="#4F46E5")
            fig.update_layout(margin=dict(l=0, r=0, t=4, b=0), height=300,
                              plot_bgcolor="white", paper_bgcolor="white",
                              xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=None),
                              yaxis=dict(title=None))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.caption(f"{len(samples)} utterances across {len(breakdown)} intents, "
                       "generated from your current profile.")

    if not latest:
        st.info("Train the model once to unlock accuracy metrics, per-intent scores and the simulator.", icon="🧠")
        return

    tab_perf, tab_matrix, tab_history, tab_prompt = st.tabs(
        ["Per-intent performance", "Confusion matrix", "Training history", "System prompt"])

    with tab_perf:
        per = latest.get("per_intent", {})
        frame = pd.DataFrame([
            {"Intent": i, "Precision %": v["precision"], "Recall %": v["recall"],
             "F1 %": v["f1"], "Test samples": v["support"]}
            for i, v in per.items()
        ]).sort_values("F1 %")
        st.dataframe(frame, use_container_width=True, hide_index=True)

    with tab_matrix:
        st.plotly_chart(_confusion_fig(latest), use_container_width=True,
                        config={"displayModeBar": False})

    with tab_history:
        hist = pd.DataFrame([{
            "Version": t.get("version", ""),
            "Trained at": (t.get("trained_at") or "").replace("T", " "),
            "Samples": t.get("samples", ""),
            "Accuracy %": t.get("accuracy", ""),
            "Macro F1 %": t.get("macro_f1", ""),
        } for t in trainings])
        st.dataframe(hist, use_container_width=True, hide_index=True)

    with tab_prompt:
        st.caption("This prompt is stored in Firebase (`users/{uid}/agentConfig/config`) and is "
                   "what a production voice stack (Twilio/Vapi + OpenAI) receives for live calls.")
        st.code(cfg.get("system_prompt", ""), language="markdown")
