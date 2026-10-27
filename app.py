"""Streamlit UI:  streamlit run app.py"""
from __future__ import annotations

import html
import re
from typing import Optional

import streamlit as st

from graph import build_graph

st.set_page_config(
    page_title="Multi-Agent Travel Planner",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS for a polished, modern UI (compatible with light & dark mode)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0284c7 100%);
        border-radius: 18px;
        padding: 1.75rem 2rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: rgba(255, 255, 255, 0.85);
        margin: 0 0 1rem 0;
        line-height: 1.5;
    }
    .pipeline-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        align-items: center;
    }
    .pipeline-pill {
        background: rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #f8fafc;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .pipeline-arrow {
        color: rgba(255, 255, 255, 0.65);
        font-size: 0.85rem;
        font-weight: 700;
    }

    /* KPI Summary Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 1rem;
        margin-bottom: 1.25rem;
    }
    .kpi-card {
        background: rgba(128, 128, 128, 0.06);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    .kpi-label {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.7;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
        line-height: 1.25;
        margin-bottom: 0.25rem;
    }
    .kpi-sub {
        font-size: 0.82rem;
        opacity: 0.78;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.18rem 0.6rem;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 600;
    }
    .badge-success {
        background: rgba(16, 185, 129, 0.16);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-warn {
        background: rgba(245, 158, 11, 0.16);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge-info {
        background: rgba(59, 130, 246, 0.16);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }

    /* Weather Cards */
    .weather-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(155px, 1fr));
        gap: 0.85rem;
        margin: 0.75rem 0 1.25rem 0;
    }
    .weather-card {
        background: rgba(128, 128, 128, 0.06);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }
    .weather-icon {
        font-size: 2rem;
        margin: 0.3rem 0;
    }
    .weather-date {
        font-size: 0.82rem;
        font-weight: 600;
        opacity: 0.8;
    }
    .weather-temp {
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0.25rem 0;
    }
    .weather-rain {
        font-size: 0.78rem;
        opacity: 0.8;
    }

    /* Budget Category Bars */
    .budget-row {
        margin-bottom: 0.85rem;
    }
    .budget-row-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 0.28rem;
    }
    .budget-bar-bg {
        width: 100%;
        height: 9px;
        background: rgba(128, 128, 128, 0.18);
        border-radius: 999px;
        overflow: hidden;
    }
    .budget-bar-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563eb, #06b6d4);
    }

    /* Agent Log Item */
    .agent-step {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.5rem;
        border-radius: 10px;
        background: rgba(128, 128, 128, 0.06);
        border-left: 4px solid #3b82f6;
        font-size: 0.88rem;
    }
    .agent-step-icon {
        font-size: 1.15rem;
        line-height: 1.2;
    }
    .agent-step-body {
        flex: 1;
    }
    .agent-step-name {
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .agent-step-msg {
        opacity: 0.85;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Constants & Helpers
# ---------------------------------------------------------------------------
AGENT_META = {
    "Supervisor": {"icon": "🎯", "color": "#6366f1"},
    "Destination Researcher": {"icon": "🔍", "color": "#0ea5e9"},
    "Weather Agent": {"icon": "🌤️", "color": "#f59e0b"},
    "Budget Planner": {"icon": "💰", "color": "#10b981"},
    "Itinerary Builder": {"icon": "🗺️", "color": "#8b5cf6"},
    "Critic": {"icon": "✅", "color": "#ec4899"},
}

PRESETS = {
    "🏔️ Mussoorie Nature & Cafes": (
        "4-day Mussoorie trip from Dehradun, 3 people, Rs 15000, we like nature and cafes"
    ),
    "🏰 Jaipur Royal Heritage": (
        "3-day Jaipur trip from Delhi, 2 people, Rs 18000, forts, local Rajasthani food and bazaars"
    ),
    "🏖️ Goa Beaches & Seafood": (
        "5-day Goa trip from Mumbai, 4 people, Rs 45000, beaches, water sports, cafes and sunset spots"
    ),
    "🌲 Manali Mountain Escape": (
        "4-day Manali trip from Chandigarh, 2 people, Rs 22000, snow views, short hikes and cozy cafes"
    ),
    "🌊 Pondicherry Coastal Vibes": (
        "3-day Pondicherry trip from Chennai, 2 people, Rs 14000, French Quarter, cycling, bakeries and beaches"
    ),
}

CATEGORY_LABELS = {
    "stay": ("🏨 Accommodation / Stay", "#3b82f6"),
    "food": ("🍽️ Food & Cafes", "#10b981"),
    "local_transport": ("🚕 Local Transport", "#f59e0b"),
    "intercity_transport": ("🚆 Intercity Travel", "#8b5cf6"),
    "activities": ("🎟️ Sightseeing & Activities", "#ec4899"),
    "contingency_5pct": ("🛡️ Contingency (5%)", "#64748b"),
}


def weather_icon_for(rain_chance: Optional[float], max_c: Optional[float], min_c: Optional[float]) -> str:
    rain = rain_chance or 0
    hi = max_c if max_c is not None else 22
    lo = min_c if min_c is not None else 12
    if rain >= 60:
        return "🌧️"
    if rain >= 35:
        return "🌦️"
    if lo <= 5:
        return "❄️"
    if hi >= 33:
        return "☀️"
    return "⛅"


def split_itinerary_days(md_text: str) -> tuple[str, list[tuple[str, str]], str]:
    """Split markdown itinerary into (intro, [(day_heading, day_body), ...], outro)."""
    pattern = re.compile(r"(?m)^##\s+(Day\s+\d+[^\n]*)$")
    matches = list(pattern.finditer(md_text))
    if not matches:
        return md_text, [], ""

    intro = md_text[: matches[0].start()].strip()
    days: list[tuple[str, str]] = []
    outro = ""

    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md_text)
        chunk = md_text[start:end].strip()

        # On the last day chunk, separate trailing "## Budget" or "## Packing" sections
        if idx == len(matches) - 1:
            sub_sec = re.search(r"(?m)^##\s+(?!Day\s+\d+)", chunk)
            if sub_sec:
                outro = chunk[sub_sec.start() :].strip()
                chunk = chunk[: sub_sec.start()].strip()

        days.append((title, chunk))

    return intro, days, outro


def render_agent_step_html(agent: str, message: str) -> str:
    meta = AGENT_META.get(agent, {"icon": "🤖", "color": "#3b82f6"})
    safe_agent = html.escape(str(agent))
    safe_msg = html.escape(str(message))
    return (
        f'<div class="agent-step" style="border-left-color: {meta["color"]};">'
        f'  <div class="agent-step-icon">{meta["icon"]}</div>'
        f'  <div class="agent-step-body">'
        f'    <div class="agent-step-name">{safe_agent}</div>'
        f'    <div class="agent-step-msg">{safe_msg}</div>'
        f"  </div>"
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
default_prompt = list(PRESETS.values())[0]
if "trip_prompt" not in st.session_state:
    st.session_state.trip_prompt = default_prompt
if "final_state" not in st.session_state:
    st.session_state.final_state = None
if "agent_events" not in st.session_state:
    st.session_state.agent_events = []

# ---------------------------------------------------------------------------
# Sidebar: Presets, Trip Builder Helper, and Agent Team Info
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧭 Trip Studio")
    st.caption("Pick a preset or build a custom prompt below.")

    st.markdown("##### ✨ Quick Presets")
    selected_preset = st.selectbox(
        "Sample trips",
        options=["Custom Prompt"] + list(PRESETS.keys()),
        index=1,
        label_visibility="collapsed",
    )
    if selected_preset != "Custom Prompt":
        if st.button("Load Preset", use_container_width=True):
            st.session_state.trip_prompt = PRESETS[selected_preset]
            st.rerun()

    st.divider()
    with st.expander("🛠️ Structured Prompt Builder", expanded=False):
        b_dest = st.text_input("Destination", value="Mussoorie")
        b_orig = st.text_input("Origin City", value="Dehradun")
        col_d, col_p = st.columns(2)
        with col_d:
            b_days = st.number_input("Days", min_value=1, max_value=15, value=4)
        with col_p:
            b_people = st.number_input("Travelers", min_value=1, max_value=20, value=3)
        b_budget = st.number_input("Total Budget (INR)", min_value=1000, step=1000, value=15000)
        b_interests = st.multiselect(
            "Interests",
            ["nature", "cafes", "history", "beaches", "adventure", "street food", "photography", "shopping"],
            default=["nature", "cafes"],
        )
        if st.button("Apply to Prompt", use_container_width=True):
            interests_str = ", ".join(b_interests) if b_interests else "sightseeing and local food"
            origin_part = f" from {b_orig}" if b_orig.strip() else ""
            st.session_state.trip_prompt = (
                f"{b_days}-day {b_dest} trip{origin_part}, {b_people} people, "
                f"Rs {b_budget}, we like {interests_str}"
            )
            st.rerun()

    st.divider()
    st.markdown("##### 🤖 Multi-Agent Team")
    for name, meta in AGENT_META.items():
        st.markdown(f"{meta['icon']} **{name}**")

# ---------------------------------------------------------------------------
# Hero Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🧭 Multi-Agent Travel Planner</div>
        <div class="hero-subtitle">
            Describe your dream getaway in plain English. A LangGraph team of 6 specialized AI agents
            researches attractions, checks live weather, calculates budgets, drafts your day-by-day plan,
            and critiques it for quality.
        </div>
        <div class="pipeline-pills">
            <span class="pipeline-pill">🎯 Supervisor</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-pill">🔍 Researcher ⚡</span>
            <span class="pipeline-pill">🌤️ Weather ⚡</span>
            <span class="pipeline-pill">💰 Budget ⚡</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-pill">🗺️ Itinerary Builder</span>
            <span class="pipeline-arrow">⇄</span>
            <span class="pipeline-pill">✅ Critic</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Trip Request Input Area
# ---------------------------------------------------------------------------
request = st.text_area(
    "✈️ Describe your trip (destination, origin, days, group size, budget & interests)",
    key="trip_prompt",
    height=95,
    placeholder="e.g. 4-day Mussoorie trip from Dehradun, 3 people, Rs 15000, we like nature and cafes",
)

btn_col1, btn_col2, _spacer = st.columns([2, 1, 5])
with btn_col1:
    run_clicked = st.button("🚀 Plan My Trip", type="primary", use_container_width=True)
with btn_col2:
    if st.session_state.final_state is not None:
        if st.button("🗑️ Clear Result", use_container_width=True):
            st.session_state.final_state = None
            st.session_state.agent_events = []
            st.rerun()

# ---------------------------------------------------------------------------
# Run LangGraph Workflow with Live Agent Streaming
# ---------------------------------------------------------------------------
if run_clicked:
    if not request.strip():
        st.warning("Please enter a trip description before planning.")
        st.stop()

    app = build_graph()
    final: dict = {}
    events: list[dict] = []

    with st.status("🤖 Multi-agent workflow in progress...", expanded=True) as status_box:
        live_feed = st.empty()
        try:
            for update in app.stream({"request": request, "agent_log": []}, stream_mode="updates"):
                for _node, data in update.items():
                    for entry in data.get("agent_log", []):
                        events.append(entry)
                        meta = AGENT_META.get(entry["agent"], {"icon": "🤖"})
                        status_box.update(
                            label=f"{meta['icon']} {entry['agent']}: {entry['message']}",
                            state="running",
                        )
                    final.update(data)

                feed_html = "".join(render_agent_step_html(e["agent"], e["message"]) for e in events)
                live_feed.markdown(feed_html, unsafe_allow_html=True)

            status_box.update(
                label=f"✨ Trip plan ready! ({len(events)} agent steps completed)",
                state="complete",
                expanded=False,
            )
            st.session_state.final_state = final
            st.session_state.agent_events = events
        except Exception as exc:
            status_box.update(label="❌ Workflow failed", state="error", expanded=True)
            st.error(f"Something went wrong: {exc}\n\nCheck your `.env` file (provider and API key).")
            st.stop()

# ---------------------------------------------------------------------------
# Render Results Dashboard
# ---------------------------------------------------------------------------
if st.session_state.final_state:
    final = st.session_state.final_state
    events = st.session_state.agent_events

    details = final.get("trip_details", {})
    budget = final.get("budget_breakdown", {})
    weather = final.get("weather", {})
    itinerary_md = final.get("itinerary", "No itinerary generated.")
    sources = final.get("sources", [])
    research_notes = final.get("research_notes", "")
    approved = final.get("approved", False)
    iterations = final.get("iterations", 1)

    dest_title = html.escape(str(details.get("destination", "Destination")).title())
    origin_title = html.escape(str(details.get("origin") or "Flexible Origin").title())
    days_count = details.get("days", "-")
    people_count = details.get("people", "-")
    interests_list = details.get("interests") or []
    interests_text = html.escape(", ".join(interests_list).title() if interests_list else "General Sightseeing")

    est_total = budget.get("total", 0)
    user_budget = budget.get("budget", details.get("budget", 0))
    within_budget = budget.get("within_budget", True)
    tier_label = str(budget.get("tier", "standard")).upper()

    budget_badge = (
        '<span class="badge badge-success">✓ Within Budget</span>'
        if within_budget
        else '<span class="badge badge-warn">⚠ Over Target Budget</span>'
    )
    critic_badge = (
        f'<span class="badge badge-success">✓ Approved (Draft #{iterations})</span>'
        if approved
        else f'<span class="badge badge-info">Refined ({iterations} drafts)</span>'
    )

    st.markdown("---")
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">📍 Route</div>
                <div class="kpi-value">{dest_title}</div>
                <div class="kpi-sub">From {origin_title}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">🗓️ Duration & Group</div>
                <div class="kpi-value">{days_count} Days · {people_count} Travelers</div>
                <div class="kpi-sub">Interests: {interests_text}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">💰 Estimated Cost</div>
                <div class="kpi-value">₹{est_total:,} <span style="font-size:0.85rem;font-weight:500;opacity:0.7;">/ ₹{user_budget:,}</span></div>
                <div class="kpi-sub">{budget_badge} &nbsp;<span class="badge badge-info">{tier_label} TIER</span></div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">🛡️ Quality Check</div>
                <div class="kpi-value">Critic Review</div>
                <div class="kpi-sub">{critic_badge}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main Organized Tabs
    tab_plan, tab_budget, tab_weather, tab_research, tab_agents = st.tabs(
        [
            "🗺️ Day-by-Day Itinerary",
            "💰 Budget Breakdown",
            "🌤️ Weather & Packing",
            "🔍 Research & Sources",
            f"🤖 Agent Trace ({len(events)})",
        ]
    )

    # --- TAB 1: Day-by-Day Itinerary ---
    with tab_plan:
        action_col1, action_col2 = st.columns([4, 1])
        with action_col1:
            st.caption("Generated by the **Itinerary Builder** and verified by the **Critic Agent**.")
        with action_col2:
            st.download_button(
                "📥 Download (.md)",
                data=itinerary_md,
                file_name=f"{details.get('destination', 'trip').lower().replace(' ', '_')}_itinerary.md",
                mime="text/markdown",
                use_container_width=True,
            )

        intro, day_sections, outro = split_itinerary_days(itinerary_md)
        if day_sections:
            if intro:
                st.markdown(intro)
            for idx, (day_title, day_body) in enumerate(day_sections):
                with st.expander(f"📅 {day_title}", expanded=(idx == 0 or len(day_sections) <= 4)):
                    st.markdown(day_body)
            if outro:
                st.divider()
                st.markdown(outro)
        else:
            st.markdown(itinerary_md)

    # --- TAB 2: Budget Breakdown ---
    with tab_budget:
        if budget:
            b_col1, b_col2 = st.columns([1, 1.3], gap="large")
            with b_col1:
                st.subheader("📊 Cost Summary")
                diff = budget.get("difference", 0)
                if within_budget:
                    st.success(f"Estimated total is **₹{diff:,} under** your ₹{user_budget:,} budget.")
                else:
                    st.warning(f"Estimated total is **₹{-diff:,} above** your ₹{user_budget:,} target budget.")

                m1, m2, m3 = st.columns(3)
                m1.metric("Travel Tier", str(budget.get("tier", "-")).title())
                m2.metric("Rooms Needed", budget.get("rooms", "-"))
                m3.metric("Nights", budget.get("nights", "-"))

                per_person = round(est_total / max(int(details.get("people", 1)), 1))
                per_day = round(est_total / max(int(details.get("days", 1)), 1))
                p1, p2 = st.columns(2)
                p1.metric("Cost per Traveler", f"₹{per_person:,}")
                p2.metric("Avg Cost per Day", f"₹{per_day:,}")

            with b_col2:
                st.subheader("🧾 Category Breakdown")
                breakdown_dict = budget.get("breakdown", {})
                bars_html = []
                for key, amount in breakdown_dict.items():
                    label, color = CATEGORY_LABELS.get(key, (key.replace("_", " ").title(), "#3b82f6"))
                    pct = min(round((amount / max(est_total, 1)) * 100, 1), 100)
                    bars_html.append(
                        f'<div class="budget-row">'
                        f'  <div class="budget-row-header">'
                        f"    <span>{label}</span>"
                        f"    <span>₹{amount:,} ({pct}%)</span>"
                        f"  </div>"
                        f'  <div class="budget-bar-bg">'
                        f'    <div class="budget-bar-fill" style="width: {pct}%; background: {color};"></div>'
                        f"  </div>"
                        f"</div>"
                    )
                st.markdown("".join(bars_html), unsafe_allow_html=True)
        else:
            st.info("No budget breakdown available.")

    # --- TAB 3: Weather & Packing ---
    with tab_weather:
        if weather.get("available"):
            st.subheader(f"🌤️ {weather.get('city', dest_title)} Forecast")
            daily_list = weather.get("daily", [])
            cards_html = ['<div class="weather-grid">']
            for day in daily_list:
                icon = weather_icon_for(day.get("rain_chance"), day.get("max_c"), day.get("min_c"))
                date_str = html.escape(str(day.get("date", "")))
                max_c = day.get("max_c", "-")
                min_c = day.get("min_c", "-")
                rain = day.get("rain_chance")
                rain_str = f"{rain}% rain" if rain is not None else "0% rain"
                cards_html.append(
                    f'<div class="weather-card">'
                    f'  <div class="weather-date">{date_str}</div>'
                    f'  <div class="weather-icon">{icon}</div>'
                    f'  <div class="weather-temp">{max_c}°C <span style="opacity:0.6;font-size:0.9rem;">/ {min_c}°C</span></div>'
                    f'  <div class="weather-rain">💧 {rain_str}</div>'
                    f"</div>"
                )
            cards_html.append("</div>")
            st.markdown("".join(cards_html), unsafe_allow_html=True)

            advice_list = weather.get("advice", [])
            st.subheader("🎒 Smart Packing & Weather Advice")
            if advice_list:
                for tip in advice_list:
                    st.info(f"💡 {tip}")
            else:
                st.success("☀️ Pleasant conditions expected! Standard comfortable travel clothing is suitable.")
        else:
            st.warning(f"Weather forecast unavailable: {weather.get('summary', 'Could not load forecast.')}")

    # --- TAB 4: Research & Sources ---
    with tab_research:
        r_col1, r_col2 = st.columns([1.6, 1], gap="large")
        with r_col1:
            st.subheader("📍 Destination Research Notes")
            if research_notes:
                st.markdown(research_notes)
            else:
                st.info("No separate research notes recorded.")
        with r_col2:
            st.subheader("🔗 Web Sources Referenced")
            if sources:
                for idx, url in enumerate(sources, start=1):
                    st.markdown(f"{idx}. [{url}]({url})")
            else:
                st.caption("No external web links returned; agent used built-in destination knowledge.")

    # --- TAB 5: Agent Trace ---
    with tab_agents:
        st.subheader("🤖 Multi-Agent Execution Timeline")
        st.caption(
            "Supervisor parses your request → Researcher, Weather, and Budget agents run in parallel → "
            "Itinerary Builder drafts the plan → Critic validates and loops if fixes are needed."
        )
        if events:
            trace_html = "".join(render_agent_step_html(e["agent"], e["message"]) for e in events)
            st.markdown(trace_html, unsafe_allow_html=True)

        if final.get("critic_feedback"):
            with st.expander("🔍 Critic Feedback History"):
                st.write(final["critic_feedback"])
else:
    # Empty-state onboarding cards before user clicks "Plan My Trip"
    st.markdown("### ✨ What you'll get in seconds")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**🗺️ Day-by-Day Plan**\n\nMorning, afternoon & evening schedules tailored to your group.")
    with c2:
        st.info("**💰 Smart Budget**\n\nTiered cost breakdown for stay, food, transport & activities in INR.")
    with c3:
        st.info("**🌤️ Live Weather**\n\nOpen-Meteo daily temperatures, rain probability & packing tips.")
    with c4:
        st.info("**✅ Critic Verified**\n\nAutomated quality checks ensure realistic timings & all days covered.")


