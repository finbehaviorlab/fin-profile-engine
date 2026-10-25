import streamlit as st
import random
import sqlite3

# ==========================================
# 1. ΒΑΣΙΚΗ ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ
# ==========================================
st.set_page_config(page_title="FinLit & Behavioral App", page_icon="💡", layout="centered")

# ==========================================
# 2. ΑΠΟΚΡΥΨΗ ΜΕΝΟΥ, HEADERS, GITHUB & ANCHORS
# ==========================================
hide_streamlit_style = """
    <style>
    header[data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    div[class^="viewerBadge_"] {display: none !important;}
    button[title="View app in GitHub"] {display: none !important;}
    a[href*="github.com"] {display: none !important;}
    [data-testid="stHeaderActionElements"] {display: none !important;}
    a.anchorjs-link {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# 3. PIN ACCESS GATEWAY
# ==========================================
CORRECT_PIN = "9218"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Behavioral Finance & Decision Profiling Engine")
    st.caption("MSc Research Prototype | Access Restricted to Authorized Reviewers")
    
    st.info("Please enter your designated 4-digit security PIN to launch the diagnostic environment.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        pin_input = st.text_input(
            "Access PIN", 
            type="password", 
            max_chars=4, 
            placeholder="Enter 4-digit PIN",
            label_visibility="collapsed"
        )
    with col2:
        submit_btn = st.button("Enter ➔", use_container_width=True)
        
    if submit_btn or pin_input:
        if pin_input == CORRECT_PIN:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid PIN. Please check your credentials.")
            
    st.stop()

# ==========================================
# 4. ΡΥΘΜΙΣΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ (SQLITE)
# ==========================================
def init_db():
    conn = sqlite3.connect("quiz_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            total_xp INTEGER,
            vulnerability_score INTEGER,
            dominant_archetype TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(name, xp, score, archetype):
    conn = sqlite3.connect("quiz_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_results (user_name, total_xp, vulnerability_score, dominant_archetype)
        VALUES (?, ?, ?, ?)
    """, (name, xp, score, archetype))
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 5. ΔΙΑΧΕΙΡΙΣΗ ΚΑΤΑΣΤΑΣΗΣ (SESSION STATE)
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = "welcome"
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "bias_score" not in st.session_state:
    st.session_state.bias_score = 0
if "bias_flags" not in st.session_state:
    st.session_state.bias_flags = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Learner"

# ==========================================
# 6. HEADER ΠΡΟΟΔΟΥ & XP
# ==========================================
if st.session_state.step not in ["welcome", "results"]:
    col1, col2 = st.columns([3, 1])
    with col1:
        progress_val = min(st.session_state.xp / 300.0, 1.0)
        st.progress(progress_val)
    with col2:
        st.metric(label="Total XP", value=f"{st.session_state.xp} / 300")
    st.markdown("---")

# ==========================================
# 7. ΟΘΟΝΕΣ ΕΦΑΡΜΟΓΗΣ (MODULAR FLOW)
# ==========================================

# --- Οθόνη 1: Welcome / Onboarding ---
if st.session_state.step == "welcome":
    st.title("🎓 FinTech Behavioral Profiler & Literacy Evaluator")
    st.caption("Master's Thesis Research Prototype | University of Piraeus")
    
    st.markdown("""
    Welcome to this interactive financial literacy and behavioral profiler. You will explore core money management concepts 
    across 3 educational levels and conclude with a behavioral decision diagnostic.
    """)
    
    st.markdown("---")
    st.subheader("📋 Evaluation Structure & Flow")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        * **Level 1:** Financial Foundations (Modules 1.1 – 1.3)
        * **Level 2:** Core Economic Mechanics (Modules 2.1 – 2.3)
        """)
    with col2:
        st.markdown("""
        * **Level 3:** Investment Principles & Portfolio Theory (Modules 3.1 – 3.3)
        * **Level 4:** Diagnostic Behavioral Bias Quizzes
        """)
        
    st.caption("⏱️ **Estimated Duration:** 4–5 minutes | **Target:** 300 Mastery XP")
    st.markdown("---")
    
    user_input = st.text_input(
        "Participant Identifier (Name or ID):", 
        value="", 
        placeholder="e.g., Alex or Participant #01"
    )
    
    st.caption("🔒 *Research Ethics & Privacy:* You may use a pseudonym or ID code. All responses are fully anonymized for academic evaluation purposes.")
    
    if st.button("Start Diagnostic Journey 🚀", use_container_width=True):
        st.session_state.user_name = user_input.strip() if user_input.strip() != "" else "Anonymous Learner"
        st.session_state.step = "m1_1_theory"
        st.rerun()

# ==============================================================================
# LEVEL 1: Financial Foundations (Personal Money Management)
# ==============================================================================

# --- Module 1.1: Saving & Personal Budgeting ---
elif st.session_state.step == "m1_1_theory":
    st.caption("Level 1: Financial Foundations | Module 1.1")
    st.header("Module 1.1: Saving & Personal Budgeting")
    st.info("🎯 **Pedagogical Objective:** Master cash-flow allocation and proactive expenditure tracking.")
    
    st.markdown("""
    * **Saving & Budgeting Principles:** Budgeting is proactively planning where each euro goes rather than wondering where it disappeared. Saving represents capital preserved untouched for future security.
    * **The 50/30/20 Framework:** Allocate net income systematically:
        * **50% Needs:** Essential expenditures (housing, utilities, groceries).
        * **30% Wants:** Discretionary lifestyle choices (dining out, entertainment, hobbies).
        * **20% Savings:** Dedicated capital for debt clearance and long-term wealth building.
    * **Emergency Reserve (Emergency Fund):** A dedicated liquid cushion equal to 3–6 months of essential living costs. It prevents forced borrowing or high-interest debt during sudden crises.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 1.1 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m1_1_quiz"
        st.session_state.pop("m1_1_status", None)
        st.rerun()

# --- Module 1.2: Debit Cards vs. Credit Cards ---
elif st.session_state.step == "m1_2_theory":
    st.caption("Level 1: Financial Foundations | Module 1.2")
    st.header("Module 1.2: Debit Cards vs. Credit Cards")
    st.info("🎯 **Pedagogical Objective:** Differentiate between self-funded transactional tools and revolving debt instruments.")
    
    st.markdown("""
    * **Debit Cards (Direct Account Deduction):** Linked directly to your depository checking balance. Transactions deduct available funds in real time without incurring debt obligations.
    * **Credit Cards (Short-Term Institutional Debt):** The financial institution settles the merchant balance on your behalf, establishing a temporary credit facility with a monthly consolidated statement.
    * **Annual Percentage Rate (APR Risk):** Carrying an unpaid balance beyond the interest-free grace period triggers high penalty APR charges, turning convenience into compounding debt.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 1.2 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m1_2_quiz"
        st.session_state.pop("m1_2_status", None)
        st.rerun()

# --- Module 1.3: Digital Banking & Payment Security ---
elif st.session_state.step == "m1_3_theory":
    st.caption("Level 1: Financial Foundations | Module 1.3")
    st.header("Module 1.3: Digital Banking & Payment Security")
    st.info("🎯 **Pedagogical Objective:** Develop cybersecurity awareness and defensive digital transaction habits.")
    
    st.markdown("""
    * **Mobile Wallets & The 'Pain of Paying':** Contactless digital payments eliminate transactional friction. However, behavioral research shows this absence of physical cash counting significantly weakens spending restraint.
    * **Credential Confidentiality & Phishing Defense:** Banking institutions never solicit secret PINs, account passwords, or One-Time Passwords (OTPs) via unsolicited links or messaging channels.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 1.3 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m1_3_quiz"
        st.session_state.pop("m1_3_status", None)
        st.rerun()

# ==============================================================================
# LEVEL 2: Core Economic Mechanics
# ==============================================================================

# --- Module 2.1: Interest Rates & Borrowing ---
elif st.session_state.step == "m2_1_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.1")
    st.header("Module 2.1: Interest Rates & Borrowing")
    st.info("🎯 **Pedagogical Objective:** Understand the dual function of interest as the cost of debt and the return on deposited capital.")
    
    st.markdown("""
    * **The Dual Nature of Interest:** 
        * For a **borrower**, interest is the price paid to an institution for utilizing borrowed funds.
        * For a **saver/lender**, interest is the return paid by the bank for deploying capital.
    * **Productive vs. Destructive Debt:**
        * **Productive Debt:** Low-cost borrowing that expands future income or assets (e.g., student loans, affordable mortgages).
        * **Destructive Debt:** High-interest credit deployed on depreciating consumer lifestyle items (e.g., credit card rollovers).
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 2.1 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m2_1_quiz"
        st.session_state.pop("m2_1_status", None)
        st.rerun()

# --- Module 2.2: The Mechanics of Inflation ---
elif st.session_state.step == "m2_2_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.2")
    st.header("Module 2.2: The Mechanics of Inflation")
    st.info("🎯 **Pedagogical Objective:** Analyze purchasing power erosion and the divergence between nominal and real values.")
    
    st.markdown("""
    * **Consumer Price Index (CPI):** Inflation measures broad price increases across goods and services over time, benchmarked systematically via the Consumer Price Index.
    * **Purchasing Power Erosion:** If capital yields 0% while inflation runs positive, the nominal figure remains identical (€100 remains €100), but its **real purchasing power** shrinks.
    * **The €100 Capital Simulation:** 
        * At a modest **4% annual inflation rate**, a basket of consumer goods costing **€100 today** will require **€104 in 1 year** and **€121.66 in 5 years**.
        * Stored idle cash steadily loses its capacity to purchase identical goods and services.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 2.2 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m2_2_quiz"
        st.session_state.pop("m2_2_status", None)
        st.rerun()

# --- Module 2.3: Compounding – Exponential Wealth Creation ---
elif st.session_state.step == "m2_3_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.3")
    st.header("Module 2.3: Compounding – Exponential Wealth Creation")
    st.info("🎯 **Pedagogical Objective:** Understand exponential growth generated by continuous reinvestment of accumulated returns.")
    
    st.markdown("""
    * **Simple vs. Compound Interest Mechanics:** 
        * **Simple Interest:** Returns accrue solely on the initial baseline principal.
        * **Compound Interest:** Returns accrue on the initial principal **plus previously accumulated returns** ("earning return on prior return").
    * **The Time Horizon Trajectory:** Reinvesting returns across extended horizons (10–30 years) converts linear gains into exponential growth. Initiating disciplined investing early maximizes this compounding multiplier.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 2.3 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m2_3_quiz"
        st.session_state.pop("m2_3_status", None)
        st.rerun()
        
# ==============================================================================
# LEVEL 3: Investment Principles & Portfolio Theory
# ==============================================================================

# --- Module 3.1: Equity Shares vs. Fixed-Income Bonds ---
elif st.session_state.step == "m3_1_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.1")
    st.header("Module 3.1: Equity Shares vs. Fixed-Income Bonds")
    st.info("🎯 **Pedagogical Objective:** Distinguish corporate equity ownership from contractual creditor debt obligations.")
    
    st.markdown("""
    * **Equity Shares (Corporate Ownership):** Represent fractional ownership in an enterprise. Shareholders participate in corporate expansion and variable dividend distributions, accompanied by market price volatility and downside risk.
    * **Fixed-Income Bonds (Debt Obligations):** Contractual debt certificates. Investors lend capital to sovereign states or corporations in exchange for periodic interest distributions (coupon payments) and full principal repayment upon maturity.
    """)
    st.caption("📚 *Institutional Reference:* Hellenic Capital Market Commission & Financial Literacy Institute (2026); Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 3.1 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m3_1_quiz"
        st.session_state.pop("m3_1_status", None)
        st.rerun()

# --- Module 3.2: The Risk-Return Spectrum ---
elif st.session_state.step == "m3_2_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.2")
    st.header("Module 3.2: The Risk-Return Spectrum")
    st.info("🎯 **Pedagogical Objective:** Master the foundational axiom linking potential investment yields to volatility and downside risk.")
    
    st.markdown("""
    * **Conceptualizing Financial Risk:** Risk represents probabilistic dispersion and capital volatility, defining the measurable uncertainty of underperformance or permanent capital loss.
    * **The Trade-Off Axiom:** Higher expected returns mathematically demand accepting greater asset price volatility and drawdown exposure. Products claiming high guaranteed returns with zero risk violate core economic theory.
    """)
    st.caption("📚 *Institutional Reference:* Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 3.2 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m3_2_quiz"
        st.session_state.pop("m3_2_status", None)
        st.rerun()

# --- Module 3.3: Portfolio Diversification & Asset Allocation ---
elif st.session_state.step == "m3_3_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.3")
    st.header("Module 3.3: Portfolio Diversification & Asset Allocation")
    st.info("🎯 **Pedagogical Objective:** Understand unsystematic risk mitigation through balanced multi-asset allocation.")
    
    st.markdown("""
    * **The Multi-Asset Principle:** Concentrating 100% of wealth into an isolated enterprise creates acute vulnerability. Distributing capital across non-correlated instruments insulates against single-firm insolvency.
    * **Unsystematic Risk Mitigation:** Allocating across diverse asset classes (equities, government debt, cash equivalents) dampens portfolio shocks. While broad macroeconomic volatility remains, company-specific ruin is eliminated.
    """)
    st.caption("📚 *Institutional Reference:* Hellenic Capital Market Commission & Financial Literacy Institute (2026); Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 3.3 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m3_3_quiz"
        st.session_state.pop("m3_3_status", None)
        st.rerun()

# ==============================================================================
# LEVEL 4: Diagnostic Behavioral Bias Screening
# ==============================================================================

elif st.session_state.step == "level_4_intro":
    st.header("Level 4: Diagnostic Behavioral Bias Screening")
    st.warning("🧠 **Transition to Behavioral Dilemmas**")
    st.write(
        "Congratulations on completing the financial literacy curriculum! Level 4 presents realistic financial dilemmas. "
        "There are no simple 'right or wrong' answers here. Choose what reflects your authentic personal reaction."
    )
    if st.button("Begin Behavioral Dilemmas (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "dilemma_1"
        st.rerun()

# --- Dilemma 4.1: Loss Aversion ---
elif st.session_state.step == "dilemma_1":
    st.caption("Dilemma 1 of 4 | Behavioral Diagnosis")
    st.subheader("Module 4.1: Loss Aversion & The Disposition Trap")
    st.caption("Prospect Theory (Kahneman & Tversky, 1979): The psychological pain of loss is approximately twice as intense as equivalent gain pleasure.")
    st.write("**Dilemma:** You bought shares in Company Alpha at €50. The price drops sharply to €35 (-30%) due to structural insolvency. Independent analysts recommend moving capital into a diversified index fund. What do you do?")
    
    options = [
        ("Sell immediately at €35, accept the loss, and reallocate capital into a diversified fund.", 0, None),
        ("Hold shares temporarily with a strict stop-loss limit to monitor movements.", 1, None),
        ("Refuse to sell until the price recovers to €50 to avoid realizing a loss on paper.", 2, "Preserver")
    ]
    
    if "d1_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d1_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d1_opts], index=None)
    
    if st.button("Confirm Choice (+15 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d1_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 15
            del st.session_state.d1_opts
            st.session_state.step = "dilemma_2"
            st.rerun()

# --- Dilemma 4.2: Herd Mentality / FOMO ---
elif st.session_state.step == "dilemma_2":
    st.caption("Dilemma 2 of 4 | Behavioral Diagnosis")
    st.subheader("Module 4.2: Herd Mentality & FOMO")
    st.caption("Herding: Aligning decisions with crowd euphoria out of fear of missing out on speculative gains.")
    st.write("**Dilemma:** A speculative crypto asset surges 400% in two weeks. Social media influencers boast quick wealth and urge buying. You have not analyzed its fundamentals. What do you do?")
    
    options = [
        ("Recognize speculative euphoria, ignore the hype, and stick to your long-term plan.", 0, None),
        ("Invest a minor, discretionary sum of pocket money that you are fully prepared to lose.", 1, None),
        ("Allocate significant personal savings immediately to avoid missing out on the rally.", 2, "Follower")
    ]
    
    if "d2_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d2_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d2_opts], index=None)
    
    if st.button("Confirm Choice (+15 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d2_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 15
            del st.session_state.d2_opts
            st.session_state.step = "dilemma_3"
            st.rerun()

# --- Dilemma 4.3: Overconfidence ---
elif st.session_state.step == "dilemma_3":
    st.caption("Dilemma 3 of 4 | Behavioral Diagnosis")
    st.subheader("Module 4.3: Overconfidence & Illusion of Control")
    st.caption("Overestimating forecasting accuracy and confusing broad market momentum with personal genius.")
    st.write("**Dilemma:** After two consecutive winning stock trades during a market rally, you feel you possess superior market timing abilities. What is your next move?")
    
    options = [
        ("Acknowledge that broad market trends drove returns, keeping core capital safely diversified.", 0, None),
        ("Commit to deeper fundamental research before deploying additional capital.", 1, None),
        ("Shift bulk savings into aggressive short-term day trading based on gut instinct.", 2, "Accumulator")
    ]
    
    if "d3_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d3_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d3_opts], index=None)
    
    if st.button("Confirm Choice (+15 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d3_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 15
            del st.session_state.d3_opts
            st.session_state.step = "dilemma_4"
            st.rerun()

# --- Dilemma 4.4: Present Bias ---
elif st.session_state.step == "dilemma_4":
    st.caption("Dilemma 4 of 4 | Behavioral Diagnosis")
    st.subheader("Module 4.4: Present Bias & Immediate Gratification")
    st.caption("Hyperbolic Discounting: Prioritizing immediate emotional consumption over distant wealth security.")
    st.write("**Dilemma:** You receive an unexpected bonus of €1,000. You currently possess no emergency reserve. How do you allocate the funds?")
    
    options = [
        ("Place the majority (€700–€800) into an emergency liquid reserve or conservative savings vehicle.", 0, None),
        ("Split the sum equally between savings reserves and personal leisure purchases.", 1, None),
        ("Spend the entire €1,000 immediately on luxury retail items, postponing savings to later.", 2, "Self-Control Deficiency")
    ]
    
    if "d4_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d4_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d4_opts], index=None)
    
    if st.button("Complete Diagnostic Evaluation (+15 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d4_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 15
            del st.session_state.d4_opts
            st.session_state.step = "results"
            st.rerun()

# ==============================================================================
# RESULTS: Behavioral Scorecard
# ==============================================================================
elif st.session_state.step == "results":
    st.balloons()
    st.title("🏆 Evaluation Complete: Behavioral Scorecard")
    st.write(f"Learner: **{st.session_state.user_name}** | Total XP Earned: **{st.session_state.xp} / 300**")
    
    score = st.session_state.bias_score
    flags = st.session_state.bias_flags
    
    if "Preserver" in flags:
        archetype = "The Preserver"
        desc = "Reluctance to realize losses and risk-averse inertia driven by Loss Aversion."
    elif "Follower" in flags:
        archetype = "The Follower"
        desc = "High susceptibility to crowd momentum, social trends, and fear of missing out (FOMO)."
    elif "Accumulator" in flags or "Self-Control Deficiency" in flags:
        archetype = "The Accumulator"
        desc = "Aggressive risk posture, overconfidence in trading, or inclination toward impulsive spending."
    else:
        archetype = "The Independent"
        desc = "Analytical, methodical decision-making with low susceptibility to emotional market traps."
        
    save_result(st.session_state.user_name, st.session_state.xp, score, archetype)
    
    st.subheader(f"Dominant Archetype: **{archetype}**")
    st.info(f"**Behavioral Profile:** {desc}")
    
    st.metric(label="Vulnerability Score (0–8 pts)", value=f"{score} / 8")
    if score <= 2:
        st.success("🟢 **Low Bias Susceptibility:** Demonstrates strong emotional discipline and objective evaluation.")
    elif score <= 5:
        st.warning("🟡 **Moderate Bias Susceptibility:** Occasional vulnerability to cognitive shortcuts; mindful review recommended.")
    else:
        st.error("🔴 **High Bias Susceptibility:** Elevated emotional sensitivity in financial environments; strict de-biasing nudges required.")
        
    st.markdown("### 🏅 Milestone Badges Earned:")
    st.markdown("- 🥉 **Financial Foundations Master** (Level 1)")
    st.markdown("- 🥈 **Economic Mechanics Expert** (Level 2)")
    st.markdown("- 🥇 **Portfolio Strategist** (Level 3)")
    st.markdown("- 🎖️ **Behavioral FinTech Diagnosed** (Level 4)")
    
    if st.button("Restart Experience 🔄", use_container_width=True):
        st.session_state.clear()
        st.rerun()
