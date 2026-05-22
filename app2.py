import streamlit as st
import os, base64

st.set_page_config(
    page_title="Prakhar Nagaich · Resume",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── PDF download helper ──────────────────────────────────────────────────────
def get_pdf_chip():
    pdf_path = "resume.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        href = f"data:application/pdf;base64,{b64}"
        return (
            f'<a class="chip chip-dl" href="{href}" '
            f'download="Prakhar_Nagaich_Resume.pdf">📄 Download Resume</a>'
        )
    return (
        '<a class="chip chip-dl chip-dl-disabled" href="#" '
        'title="Place resume.pdf in the app directory to enable download" '
        'onclick="return false;">📄 Download Resume</a>'
    )

# ── Placeholder project URL — replace per project when prototype is ready ────
PROJECT_URL = "https://www.youtube.com"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #d8e6f0; }
.main, [data-testid="stAppViewContainer"] { background: #06090f; }
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
.stMarkdown { margin: 0 !important; }
footer { display: none; }

/* ── TABS ── */
[data-testid="stTabs"] {
    background: rgba(6,9,15,0.97);
    border-bottom: 1px solid #1a2840;
    position: sticky; top: 0; z-index: 99;
    padding: 0;
}
div[role="tablist"] {
    justify-content: center !important;
    border-bottom: none !important;
    gap: 0 !important;
}
button[data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #6b8099 !important;
    background: transparent !important;
    border: none !important;
    padding: 20px 32px !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    transition: color 0.2s !important;
}
button[data-baseweb="tab"]:hover { color: #00c8ff !important; }
button[aria-selected="true"][data-baseweb="tab"] {
    color: #00c8ff !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #00c8ff !important;
}
[data-testid="stTabPanel"] { padding: 0 !important; }

/* ── HERO ── */
.hero {
    background: linear-gradient(160deg, #08111f 0%, #060a14 50%, #080d1a 100%);
    border-bottom: 1px solid #111e33;
    padding: 80px 40px 72px;
    text-align: center;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; letter-spacing: 0.22em;
    text-transform: uppercase; color: #00c8ff;
    margin-bottom: 18px;
    display: flex; align-items: center; justify-content: center; gap: 12px;
}
.hero-eyebrow::before,
.hero-eyebrow::after {
    content: ''; display: inline-block;
    width: 28px; height: 1px; background: #00c8ff;
}
.hero-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4.5rem, 9vw, 8rem);
    line-height: 0.9; letter-spacing: 0.02em; color: #e8f0f8;
    margin-bottom: 28px;
}
.hero-bio {
    font-size: 1.02rem;
    color: #6b8099;
    max-width: 880px;
    line-height: 1.78;
    margin: 0 auto 32px;
}
.hero-bio strong { color: #adc4d8; font-weight: 500; }

/* ── CHIPS ── */
.contact-row {
    display: flex; gap: 10px; flex-wrap: wrap;
    margin-bottom: 48px; justify-content: center; align-items: center;
}
.chip {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 7px 16px;
    background: rgba(0,200,255,0.06);
    border: 1px solid rgba(0,200,255,0.2);
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; color: #4aaccc;
    text-decoration: none;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s, color 0.2s;
    white-space: nowrap;
}
a.chip:hover {
    background: rgba(0,200,255,0.14);
    border-color: rgba(0,200,255,0.45);
    color: #7adcf5;
}
.chip-dl {
    background: rgba(123,94,167,0.08);
    border-color: rgba(123,94,167,0.3);
    color: #a07fd4;
}
a.chip-dl:hover {
    background: rgba(123,94,167,0.18);
    border-color: rgba(123,94,167,0.55);
    color: #c4a8e8;
}
.chip-dl-disabled { opacity: 0.45; cursor: not-allowed !important; }

/* ── STATS ── */
.stats-row {
    display: flex; gap: 48px; flex-wrap: wrap;
    padding-top: 32px; border-top: 1px solid #111e33;
    justify-content: center;
}
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem; line-height: 1; color: #e8f0f8;
}
.stat-num em { color: #00c8ff; font-style: normal; }
.stat-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem; color: #3d5570;
    text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px;
}

/* ── SECTION WRAPPERS ── */
.sec-wrap {
    padding: 64px 10% 72px;
    border-bottom: 1px solid #0e1824; background: #06090f;
}
.sec-wrap.alt { background: #07090f; }
.sec-label {
    display: flex; align-items: center; gap: 14px; margin-bottom: 10px;
}
.sec-label-txt {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem; color: #00c8ff;
    letter-spacing: 0.2em; text-transform: uppercase; white-space: nowrap;
}
.sec-lbl-line { flex: 1; height: 1px; background: linear-gradient(90deg, #1a2840, transparent); }
.sec-lbl-num { font-family: 'JetBrains Mono', monospace; font-size: 0.63rem; color: #253545; }
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem; letter-spacing: 0.04em; color: #e8f0f8;
    margin-bottom: 36px; line-height: 1;
}

/* ── IMPACT GRID ── */
.impact-row {
    display: grid; grid-template-columns: repeat(5, 1fr);
    border: 1px solid #111e33; border-radius: 12px; overflow: hidden;
}
.ic {
    padding: 32px 16px; text-align: center;
    border-right: 1px solid #111e33; background: #080d18;
}
.ic:last-child { border-right: none; }
.ic-num {
    font-family: 'Bebas Neue', sans-serif; font-size: 2.4rem;
    color: #e8f0f8; line-height: 1; margin-bottom: 8px;
}
.ic-num em { color: #00c8ff; font-style: normal; }
.ic-lbl {
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
    color: #3d5570; text-transform: uppercase; letter-spacing: 0.08em; line-height: 1.45;
}

/* ── STRENGTH GRID ── */
.sgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.sb {
    background: #080d18; border: 1px solid #111e33;
    border-radius: 12px; padding: 26px 30px;
    border-top: 2px solid #00c8ff;
}
.sb.b { border-top-color: #7b5ea7; }
.sb-ttl {
    font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
    color: #00c8ff; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 12px;
}
.stags { display: flex; flex-wrap: wrap; gap: 7px; }
.stg {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    padding: 5px 12px; background: #0c1522; border: 1px solid #1a2840;
    border-radius: 6px; color: #5a7a95;
}

/* ── EXPERIENCE ── */
.exp-card {
    background: #080d18; border: 1px solid #111e33;
    border-left: 3px solid #00c8ff; border-radius: 0 12px 12px 0;
    padding: 32px 36px; margin-bottom: 16px;
}
.exp-card.sec { border-left-color: #7b5ea7; }
.exp-hdr {
    display: flex; justify-content: space-between;
    align-items: flex-start; flex-wrap: wrap; gap: 12px;
    margin-bottom: 18px; padding-bottom: 18px; border-bottom: 1px solid #0e1824;
}
.exp-co {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.9rem;
    letter-spacing: 0.06em; color: #e8f0f8; line-height: 1;
}
.exp-role { font-size: 0.83rem; color: #00c8ff; font-weight: 500; margin-top: 5px; }
.exp-per {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    color: #3d5570; background: #0c1522; border: 1px solid #111e33;
    border-radius: 6px; padding: 5px 12px; white-space: nowrap; align-self: flex-start;
}
.sub-lbl {
    font-family: 'JetBrains Mono', monospace; font-size: 0.63rem;
    color: #7b5ea7; letter-spacing: 0.18em; text-transform: uppercase;
    margin: 18px 0 10px;
}
.sub-lbl.c { color: #00c8ff; margin-top: 0; }
.bul {
    display: flex; gap: 12px; margin-bottom: 9px;
    font-size: 0.86rem; color: #6b8099; line-height: 1.65;
}
.arr { color: #00c8ff; flex-shrink: 0; margin-top: 2px; font-size: 0.72rem; }
.bul b { color: #adc4d8; font-weight: 500; }
.trow {
    display: flex; flex-wrap: wrap; gap: 7px;
    margin-top: 18px; padding-top: 18px; border-top: 1px solid #0e1824;
}
.et {
    font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
    padding: 4px 11px; border-radius: 5px;
    background: rgba(0,200,255,0.06); border: 1px solid rgba(0,200,255,0.15); color: #3a90aa;
}
.et.p { background: rgba(123,94,167,0.07); border-color: rgba(123,94,167,0.2); color: #8f70c0; }
.et.r { background: rgba(224,78,107,0.06); border-color: rgba(224,78,107,0.15); color: #b85c72; }

/* ── PROJECT CARDS ── */
/*  Fix overlaps: box-sizing, overflow, word-break, consistent padding  */
a.pc-link {
    display: block;
    text-decoration: none;
    border-radius: 12px;
    transition: transform 0.18s, box-shadow 0.18s;
}
a.pc-link:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,200,255,0.12);
}
a.pc-link:hover .pc {
    border-top-color: rgba(0,200,255,0.8);
    background: #0a1220;
}
.pc {
    background: #080d18;
    border: 1px solid #111e33;
    border-radius: 12px;
    padding: 24px;
    border-top: 2px solid rgba(0,200,255,0.3);
    box-sizing: border-box;          /* prevents content from spilling outside */
    overflow: hidden;                /* clips anything that still overflows    */
    transition: background 0.18s, border-top-color 0.18s;
}
.pc-top {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 14px;
}
.pc-icon {
    width: 38px; height: 38px;
    background: rgba(0,200,255,0.07); border: 1px solid rgba(0,200,255,0.15);
    border-radius: 9px; display: flex; align-items: center;
    justify-content: center; font-size: 1rem; flex-shrink: 0;
}
.pc-dt { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #253545; }
.pc-name {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.25rem;
    letter-spacing: 0.05em; color: #e8f0f8;
    margin-bottom: 3px; line-height: 1.1;
    white-space: normal; word-break: break-word;
}
.pc-type {
    font-family: 'JetBrains Mono', monospace; font-size: 0.63rem;
    color: #00c8ff; letter-spacing: 0.1em; margin-bottom: 16px;
}
.pf {
    display: flex; gap: 8px; font-size: 0.79rem;
    color: #4a6a85; margin-bottom: 6px; line-height: 1.5;
    word-break: break-word;        /* stops long phrases overflowing the card */
    overflow-wrap: break-word;
}
.pf::before {
    content: '◈'; color: #7b5ea7; font-size: 0.48rem;
    margin-top: 4px; flex-shrink: 0;
}
/* small "View Prototype" footer on each card */
.pc-cta {
    margin-top: 16px; padding-top: 12px; border-top: 1px solid #0e1824;
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
    color: #2a6a80; letter-spacing: 0.12em; text-transform: uppercase;
    display: flex; align-items: center; gap: 5px;
}
.pc-cta::before { content: '↗'; color: #00c8ff; font-size: 0.65rem; }

/* ── EDUCATION ── */
.edu {
    background: #080d18; border: 1px solid #111e33; border-radius: 12px;
    padding: 24px 30px; margin-bottom: 12px;
    display: flex; justify-content: space-between; align-items: center;
    gap: 20px; flex-wrap: wrap;
}
.edu-deg {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.15rem;
    letter-spacing: 0.05em; color: #e8f0f8; margin-bottom: 4px;
}
.edu-inst { font-size: 0.8rem; color: #4a6a85; }
.edu-bdg {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    padding: 5px 14px; border-radius: 999px;
    background: rgba(123,94,167,0.08); border: 1px solid rgba(123,94,167,0.25); color: #8f70c0;
    white-space: nowrap;
}
.cert {
    background: #080d18; border: 1px solid #111e33;
    border-left: 3px solid #00c8ff; border-radius: 0 10px 10px 0;
    padding: 16px 26px; margin-bottom: 10px;
    display: flex; align-items: center; gap: 12px;
    font-size: 0.86rem; color: #5a7a95;
}
.cert::before { content: '✦'; color: #00c8ff; font-size: 0.68rem; flex-shrink: 0; }

/* ── FOOTER ── */
.ft {
    text-align: center; padding: 32px 40px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
    color: #253545; letter-spacing: 0.1em; background: #06090f;
    border-top: 1px solid #0e1824;
}

/* column gap/padding reset (skills + project columns) */
div[data-testid="stHorizontalBlock"] { gap: 12px !important; padding: 0 10% !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">Product Manager · GenAI &amp; Enterprise SaaS</div>
  <div class="hero-name">Prakhar Nagaich</div>
  <div class="hero-bio">
    <strong>8+ years</strong> architecting high-impact <strong>B2B SaaS and Enterprise digital products</strong>,
    bridging <strong>Product Management and Applied GenAI</strong> to transform complex business needs into scalable,
    revenue-generating solutions. Proven 0→1 track record leading cross-functional teams across Tech, HR, E-commerce
    and L&amp;D — with deep expertise in <strong>Integrations, Cloud platforms, Requirement Management and Wireframing</strong>,
    underpinned by KPI-driven, data-first decision-making.
  </div>
  <div class="contact-row">
    <a class="chip" href="tel:+918527710741">📞 +91 85277 10741</a>
    <a class="chip" href="mailto:pgp09prakharn@iimrohtak.ac.in">✉️ pgp09prakharn@iimrohtak.ac.in</a>
    <a class="chip" href="https://linkedin.com/in/prakharnagaich" target="_blank" rel="noopener noreferrer">🔗 linkedin.com/in/prakharnagaich</a>
    {get_pdf_chip()}
  </div>
  <div class="stats-row">
    <div><div class="stat-num">8<em>+</em></div><div class="stat-lbl">Years Experience</div></div>
    <div><div class="stat-num">500<em>K+</em></div><div class="stat-lbl">Platform Users</div></div>
    <div><div class="stat-num">$550<em>K</em></div><div class="stat-lbl">ARR Generated</div></div>
    <div><div class="stat-num">20<em>+</em></div><div class="stat-lbl">Enterprise Clients</div></div>
    <div><div class="stat-num">40<em>+</em></div><div class="stat-lbl">Team Members</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡   Impact",
    "💼   Experience",
    "🚀   Projects",
    "🧠   Skills",
    "🎓   Education",
])

# ═════════════════════════════════════════════════
# TAB 1 — IMPACT
# ═════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="sec-wrap">
      <div class="sec-label">
        <span class="sec-label-txt">Impact at a Glance</span>
        <div class="sec-lbl-line"></div>
        <span class="sec-lbl-num">01</span>
      </div>
      <div class="sec-title">Numbers That Matter</div>
      <div class="impact-row">
        <div class="ic"><div class="ic-num">85<em>%</em></div><div class="ic-lbl">Campus Interviews Automated</div></div>
        <div class="ic"><div class="ic-num">↓55<em>%</em></div><div class="ic-lbl">Handle Time Reduction</div></div>
        <div class="ic"><div class="ic-num">65<em>%</em></div><div class="ic-lbl">Assessments Auto-Generated</div></div>
        <div class="ic"><div class="ic-num">↓66<em>%</em></div><div class="ic-lbl">Hire-to-Deploy Cycle Cut</div></div>
        <div class="ic"><div class="ic-num">22<em>%</em></div><div class="ic-lbl">Content Completion Boost</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sec-wrap alt" style="border-top:1px solid #0e1824;">
      <div class="sec-label">
        <span class="sec-label-txt">Core Strengths</span>
        <div class="sec-lbl-line"></div>
      </div>
      <div class="sec-title">What I Bring</div>
      <div class="sgrid">
        <div class="sb">
          <div class="sb-ttl"> Applied GenAI</div>
          <div style="font-size:0.87rem;color:#4a6a85;line-height:1.75">
            RAG pipelines · fine-tuning · Agentic AI · MLOps · Virtual agents · LLM and SLM ·
            Prototyping · Document validation · Recommendation engines
          </div>
        </div>
        <div class="sb b">
          <div class="sb-ttl"> Product Strategy</div>
          <div style="font-size:0.87rem;color:#4a6a85;line-height:1.75">
            0→1 launches · Enterprise SaaS · B2B roadmaps · Stakeholder Management · Requirement Gathering/BRD ·
            Cross-functional leadership · OKR/KPI alignment · Backlog Management · 40+ team management
          </div>
        </div>
        <div class="sb b">
          <div class="sb-ttl"> Technical Fluency</div>
          <div style="font-size:0.87rem;color:#4a6a85;line-height:1.75">
            REST APIs · Cloud (GCP/Azure) · SQL · JIRA/ADO ·
            UI/UX wireframing · Agile/Scrum · Integration architecture
          </div>
        </div>
        <div class="sb">
          <div class="sb-ttl"> Domain Coverage</div>
          <div style="font-size:0.87rem;color:#4a6a85;line-height:1.75">
            HR Tech · EdTech / L&amp;D · E-commerce ·
            Enterprise digital transformation · GDPR / SOC2 compliance
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════
# TAB 2 — EXPERIENCE
# ═════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="sec-wrap">
      <div class="sec-label">
        <span class="sec-label-txt">Work Experience</span>
        <div class="sec-lbl-line"></div>
        <span class="sec-lbl-num">02</span>
      </div>
      <div class="sec-title">Where I've Built</div>

      <div class="exp-card">
        <div class="exp-hdr">
          <div>
            <div class="exp-co">Cognizant</div>
            <div class="exp-role">Product Manager / Manager Business Analyst</div>
          </div>
          <div class="exp-per">Jul 2020 – Present</div>
        </div>
        <div class="sub-lbl c">/ AI Transformation</div>
        <div class="bul"><span class="arr">→</span><span>Own GenAI initiatives — Virtual Interview Agent, Assessment Builder, Forensic Tool, Personal Assistant — integrated into Enterprise and Learning platforms.</span></div>
        <div class="bul"><span class="arr">→</span><span>Optimised AI Personal Assistant via RAG pipelines and LLM fine-tuning: <b>↓25% resolution time, ↓55% average handle time</b>, improved Customer Effort Score.</span></div>
        <div class="bul"><span class="arr">→</span><span>Launched GenAI virtual interviewer handling <b>85% of Level 1 campus interviews</b> at Cognizant.</span></div>
        <div class="bul"><span class="arr">→</span><span>Spearheaded AI-powered assessment platform enabling <b>65% of evaluations autonomously generated</b>.</span></div>
        <div class="bul"><span class="arr">→</span><span>Delivered cross-model analytics dashboard monitoring AI response latency, API switching and cost efficiency across production LLM deployments.</span></div>
        <div class="bul"><span class="arr">→</span><span>Recommendation engine drove <b>11% increase</b> in avg content consumption across a <b>1M+ user</b> platform.</span></div>
        <div class="bul"><span class="arr">→</span><span>Restructured requirement documentation with GenAI tooling, <b>increasing team velocity by 20%</b> without additional headcount.</span></div>
        <div class="sub-lbl">/ Product Strategy</div>
        <div class="bul"><span class="arr">→</span><span>Led 3 Product Owners managing L&amp;D solutions portfolio — generated <b>~$550K ARR</b> from 30+ enterprise clients; managed 40+ team members, ~$400K annual budget.</span></div>
        <div class="bul"><span class="arr">→</span><span>Scaled enterprise LMS delivering <b>~$180K + $290K annual cost savings</b> by reducing third-party product reliance.</span></div>
        <div class="bul"><span class="arr">→</span><span>Behaviour-driven engagement layer within LMS boosted <b>content completion rates by 22%</b>.</span></div>
        <div class="bul"><span class="arr">→</span><span>Optimised onboarding product achieving <b>average 66% decrease</b> in Hire-to-Deploy cycle time.</span></div>
        <div class="bul"><span class="arr">→</span><span>Achieved <b>70% feature adoption</b> within first 2 months of mentorship module launch.</span></div>
        <div class="trow">
          <span class="et">GenAI</span><span class="et">RAG</span><span class="et">LLM Fine-tuning</span><span class="et">Stakeholder Management</span>
          <span class="et">Enterprise and SaaS Product</span><span class="et p">LLM</span><span class="et p">Product Lifecycle Management</span>
          <span class="et p">HRTech</span><span class="et r">EdTech</span><span class="et r">API and SQL</span><span class="et r">Design and Prototype</span>
        </div>
      </div>

      <div class="exp-card sec">
        <div class="exp-hdr">
          <div>
            <div class="exp-co">Mindtree</div>
            <div class="exp-role">Senior Engineer</div>
          </div>
          <div class="exp-per">Feb 2016 – Jun 2018</div>
        </div>
        <div class="sub-lbl c">/ Engineering</div>
        <div class="bul"><span class="arr">→</span><span>Testing and implementation of various modules on Oracle's SAAS HR product — HCM Fusion.</span></div>
        <div class="bul"><span class="arr">→</span><span>Spearheaded migration of critical data to a new platform while maintaining system stability and minimal user impact.</span></div>
        <div class="bul"><span class="arr">→</span><span>Engineered a comprehensive HR reporting ecosystem to enhance data-driven decision-making for the client.</span></div>
        <div class="trow">
          <span class="et p">Oracle HCM Fusion</span>
          <span class="et">Data Migration</span>
          <span class="et p">HR Analytics</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════
# TAB 3 — PROJECTS  (original st.columns approach, anchor-wrapped, overlap fixed)
# ═════════════════════════════════════════════════
with tab3:
    # Section header — same padding/style as every other tab
    st.markdown("""
    <div class="sec-wrap" style="padding-bottom:8px;">
      <div class="sec-label">
        <span class="sec-label-txt">Projects</span>
        <div class="sec-lbl-line"></div>
        <span class="sec-lbl-num">03</span>
      </div>
      <div class="sec-title">What I've Shipped</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1 ──────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <a class="pc-link" href="{PROJECT_URL}" target="_blank" rel="noopener noreferrer">
          <div class="pc">
            <div class="pc-top">
              <div class="pc-icon">🎓</div>
              <div class="pc-dt">Aug 2020 – Present</div>
            </div>
            <div class="pc-name">SkillSpring / My Learning Studio</div>
            <div class="pc-type">LMS · In-house + SaaS</div>
            <div class="pf">Mentoring Platform — structured connections and mentorship</div>
            <div class="pf">Learning Paths — curated sequences aligned to career tracks</div>
            <div class="pf">Recommendation Engine — AI personalised content suggestions</div>
            <div class="pf">Assessment Builder — adaptive GenAI evaluation platform</div>
            <div class="pf">Reels — Instagram-style short learning modules</div>
            <div class="pc-cta">View Prototype</div>
          </div>
        </a>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <a class="pc-link" href="{PROJECT_URL}" target="_blank" rel="noopener noreferrer">
          <div class="pc">
            <div class="pc-top">
              <div class="pc-icon">🔬</div>
              <div class="pc-dt">Aug 2025 – Present</div>
            </div>
            <div class="pc-name">Proof AI</div>
            <div class="pc-type">Agentic Validation · In-house</div>
            <div class="pf">Custom Agents — grouped agentic workflows with governance</div>
            <div class="pf">Workflow Agnostic — API-based plug-and-play validation</div>
            <div class="pf">Extensible Framework — pluggable third-party agent architecture</div>
            <div class="pc-cta">View Prototype</div>
          </div>
        </a>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <a class="pc-link" href="{PROJECT_URL}" target="_blank" rel="noopener noreferrer">
          <div class="pc">
            <div class="pc-top">
              <div class="pc-icon">🤖</div>
              <div class="pc-dt">Jun 2024 – Aug 2025</div>
            </div>
            <div class="pc-name">AI Interview Agent</div>
            <div class="pc-type">GenAI · In-house</div>
            <div class="pf">GenAI Virtual Interviewer simulating real interview dynamics</div>
            <div class="pf">Speech-to-Text and Text-to-Speech for voice interaction</div>
            <div class="pf">Handles 85% of Level 1 campus recruitment at Cognizant</div>
            <div class="pc-cta">View Prototype</div>
          </div>
        </a>
        """, unsafe_allow_html=True)

    # ── Row 2 (2 cards, third column left intentionally empty) ──
    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown(f"""
        <a class="pc-link" href="{PROJECT_URL}" target="_blank" rel="noopener noreferrer">
          <div class="pc">
            <div class="pc-top">
              <div class="pc-icon">💬</div>
              <div class="pc-dt">Nov 2023 – Jan 2025</div>
            </div>
            <div class="pc-name">Personalized Assistant</div>
            <div class="pc-type">RAG · In-house + SaaS</div>
            <div class="pf">Vector and vector-less RAG pipelines with LLM fine-tuning</div>
            <div class="pf">Manages timesheets, learning suggestions, query resolution</div>
            <div class="pf">↓25% resolution time · ↓55% average handle time</div>
            <div class="pc-cta">View Prototype</div>
          </div>
        </a>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <a class="pc-link" href="{PROJECT_URL}" target="_blank" rel="noopener noreferrer">
          <div class="pc">
            <div class="pc-top">
              <div class="pc-icon">🎯</div>
              <div class="pc-dt">Dec 2022 – Nov 2023</div>
            </div>
            <div class="pc-name">Campus Recruit</div>
            <div class="pc-type">HR Tech · In-house</div>
            <div class="pf">Hire-to-Deploy mapping — demand collation and resource alignment</div>
            <div class="pf">Campus Engagement — graduate query handling and automation</div>
            <div class="pc-cta">View Prototype</div>
          </div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════
# TAB 4 — SKILLS
# ═════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="sec-wrap" style="padding-bottom:8px;">
      <div class="sec-label">
        <span class="sec-label-txt">Skills &amp; Tools</span>
        <div class="sec-lbl-line"></div>
        <span class="sec-lbl-num">04</span>
      </div>
      <div class="sec-title">Tools of the Trade</div>
    </div>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""
        <div class="sb" style="margin-bottom:12px;">
          <div class="sb-ttl"> GenAI &amp; ML</div>
          <div class="stags">
            <span class="stg">RAG</span><span class="stg">Fine-tuning</span>
            <span class="stg">LLM</span><span class="stg">SLM</span>
            <span class="stg">OpenAI</span><span class="stg">Gemini</span>
            <span class="stg">LLaMA</span><span class="stg">Agentic AI</span>
            <span class="stg">Orchestrators</span><span class="stg">MLOps</span>
            <span class="stg">Prototyping</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="sb b">
          <div class="sb-ttl"> Technical &amp; Tools</div>
          <div class="stags">
            <span class="stg">REST API</span><span class="stg">Integration</span>
            <span class="stg">UI/UX</span><span class="stg">SQL</span>
            <span class="stg">JIRA/ADO</span><span class="stg">Agile/Scrum</span>
            <span class="stg">User Stories</span><span class="stg">GCP</span>
            <span class="stg">Azure</span><span class="stg">Wireframing</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="sb b" style="margin-bottom:12px;">
          <div class="sb-ttl"> Product Management</div>
          <div class="stags">
            <span class="stg">Product Lifecycle</span><span class="stg">Market Research</span>
            <span class="stg">Backlog Mgmt</span><span class="stg">Roadmap</span>
            <span class="stg">Stakeholder Mgmt</span><span class="stg">Enterprise SaaS</span>
            <span class="stg">GDPR</span><span class="stg">Product Adoption</span>
            <span class="stg">BRD</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="sb">
          <div class="sb-ttl"> Domain Expertise</div>
          <div class="stags">
            <span class="stg">HR Tech</span><span class="stg">EdTech</span>
            <span class="stg">E-commerce</span><span class="stg">L&amp;D</span>
            <span class="stg">B2B SaaS</span>
            <span class="stg">Digital Transformation</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════
# TAB 5 — EDUCATION
# ═════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div class="sec-wrap">
      <div class="sec-label">
        <span class="sec-label-txt">Education &amp; Certifications</span>
        <div class="sec-lbl-line"></div>
        <span class="sec-lbl-num">05</span>
      </div>
      <div class="sec-title">Academic Foundation</div>
      <div class="edu">
        <div>
          <div class="edu-deg">PGDM — Marketing Strategy &amp; MIS</div>
          <div class="edu-inst">IIM Rohtak</div>
        </div>
        <div class="edu-bdg">Post Graduate</div>
      </div>
      <div class="edu">
        <div>
          <div class="edu-deg">B.Tech — Electronics &amp; Communication Engineering</div>
          <div class="edu-inst">Jaypee Institute of Information Technology</div>
        </div>
        <div class="edu-bdg">Undergraduate</div>
      </div>
      <div style="height:24px"></div>
      <div class="cert">Certified Scrum Product Owner (CSPO)</div>
      <div class="cert">Certified SAFe Product Owner / Product Manager</div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="ft">
  Prakhar Nagaich &nbsp;·&nbsp; Product Manager &nbsp;·&nbsp;
  GenAI &amp; Enterprise SaaS &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)
