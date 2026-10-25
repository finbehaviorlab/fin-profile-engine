import streamlit as st
import random
import sqlite3

# ==========================================
# PIN ACCESS GATEWAY
# ==========================================
CORRECT_PIN = "9218"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Restricted Access")
    st.info("Please enter the access PIN to continue to the application.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        pin_input = st.text_input(
            "Access PIN", 
            type="password", 
            max_chars=4, 
            placeholder="Enter 4-digit PIN"
        )
    with col2:
        st.write("")  # Vertical spacing for alignment
        st.write("")
        submit_btn = st.button("Enter", use_container_width=True)
        
    if submit_btn or pin_input:
        if pin_input == CORRECT_PIN:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid PIN. Please try again.")
            
    # Halts execution of the rest of the script until authenticated
    st.stop()
# ==========================================

# --- 1. ΡΥΘΜΙΣΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ (SQLITE) ---
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

# --- 2. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ STREAMLIT ---
st.set_page_config(page_title="FinLit & Behavioral App", page_icon="💡", layout="centered")

# ==========================================
# HIDE STREAMLIT BRANDING & SOURCE CODE LINK
# ==========================================
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none;}
    [data-testid="stToolbar"] {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# ==========================================

# --- 3. ΔΙΑΧΕΙΡΙΣΗ ΚΑΤΑΣΤΑΣΗΣ (SESSION STATE) ---
if "step" not in st.session_state:
    st.session_state.step = "welcome"
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "bias_score" not in st.session_state:
    st.session_state.bias_score = 0
if "bias_flags" not in st.session_state:
    st.session_state.bias_flags = []
if "current_level" not in st.session_state:
    st.session_state.current_level = 1
if "user_name" not in st.session_state:
    st.session_state.user_name = "Learner"

# --- 4. HEADER ΠΡΟΟΔΟΥ & XP ---
if st.session_state.step not in ["welcome", "results"]:
    col1, col2 = st.columns([3, 1])
    with col1:
        progress_val = min(st.session_state.xp / 300.0, 1.0)
        st.progress(progress_val)
    with col2:
        st.metric(label="Total XP", value=f"{st.session_state.xp} / 300")
    st.markdown("---")

# --- 5. ΟΘΟΝΕΣ ΕΦΑΡΜΟΓΗΣ ---

# Οθόνη 1: Welcome / Onboarding
if st.session_state.step == "welcome":
    st.title("🎓 FinTech Learning & Behavioral Bias Screener")
    st.subheader("Master foundational finance and discover your financial mindset.")
    st.write(
        "Welcome! This interactive micro-learning prototype guides you through essential money principles "
        "and evaluates behavioral decision patterns across 4 progressive levels."
    )
    user_input = st.text_input("Enter your name to begin:", value="Learner")
    if st.button("Start Journey 🚀", use_container_width=True):
        st.session_state.user_name = user_input
        st.session_state.step = "level_1_cards"
        st.rerun()

# Οθόνη 2: Level 1 - Learning Cards (Financial Foundations)
elif st.session_state.step == "level_1_cards":
    st.header("Level 1: Financial Foundations")
    st.info("💡 **Core Rules of Cash Flow & Liquidity**")
    
    st.markdown("""
    * **Saving & Budgeting (50/30/20 Rule):** Allocate 50% of your net income to Needs, 30% to Wants, and 20% to Savings.
    * **Emergency Reserve:** Build a liquid cushion covering 3–6 months of essential living costs for unforeseen crises.
    * **Debit vs. Credit Cards:** Debit cards spend your existing bank funds immediately. Credit cards utilize borrowed bank capital that accrues high interest (APR) if unpaid.
    * **Digital Banking Security:** Never disclose PINs, one-time passwords, or account credentials to third parties or unsolicited links.
    """)
    
    if st.button("Proceed to Knowledge Checkpoint (+30 XP)", use_container_width=True):
        st.session_state.xp += 30
        st.session_state.step = "level_1_quiz"
        st.rerun()

# Οθόνη 3: Level 1 - Quiz Checkpoint
elif st.session_state.step == "level_1_quiz":
    st.header("Level 1 Checkpoint: Cash Flow")
    st.write("**Question:** What is the primary function of establishing an emergency fund (reserve)?")
    
    ans = st.radio(
        "Select the correct answer:",
        [
            "To maximize high-risk speculative trading opportunities.",
            "To provide a liquid cash cushion covering 3–6 months of essential living expenses during unforeseen crises.",
            "To purchase luxury lifestyle items without waiting."
        ],
        index=None
    )
    
    if st.button("Submit Answer", use_container_width=True):
        if ans == "To provide a liquid cash cushion covering 3–6 months of essential living expenses during unforeseen crises.":
            st.success("Correct! Emergency reserves ensure defensive liquidity without relying on high-interest debt.")
            st.session_state.xp += 20
            st.session_state.step = "level_2_cards"
            st.rerun()
        elif ans is not None:
            st.error("Incorrect. An emergency reserve must strictly cover 3–6 months of essential needs in liquid cash.")
            if st.button("Continue to Level 2"):
                st.session_state.step = "level_2_cards"
                st.rerun()

# Οθόνη 4: Level 2 - Learning Cards (Economic Mechanics)
elif st.session_state.step == "level_2_cards":
    st.header("Level 2: Core Economic Mechanics")
    st.info("📈 **The Time Value of Money**")
    
    st.markdown("""
    * **Inflation (The Silent Tax):** A general increase in prices measured by the CPI. Uninvested cash at 0% interest loses purchasing power over time.
    * **Dual Role of Interest:** Interest represents the cost of borrowing for a debtor and the reward for lending/saving for a depositor.
    * **Compounding Wealth:** Earning interest on previously accumulated interest creates non-linear exponential growth over long investment horizons.
    """)
    
    if st.button("Proceed to Knowledge Checkpoint (+30 XP)", use_container_width=True):
        st.session_state.xp += 30
        st.session_state.step = "level_2_quiz"
        st.rerun()

# Οθόνη 5: Level 2 - Quiz Checkpoint
elif st.session_state.step == "level_2_quiz":
    st.header("Level 2 Checkpoint: Inflation & Compounding")
    st.write("**Question:** If annual inflation averages 4% while cash remains stored uninvested at 0% return, what occurs to your capital over time?")
    
    ans = st.radio(
        "Select the correct answer:",
        [
            "The purchasing power decreases, meaning the same nominal money buys fewer goods and services.",
            "The nominal value of cash automatically increases to match inflation.",
            "Purchasing power remains completely unchanged."
        ],
        index=None
    )
    
    if st.button("Submit Answer", use_container_width=True):
        if ans == "The purchasing power decreases, meaning the same nominal money buys fewer goods and services.":
            st.success("Correct! Real purchasing power deteriorates if returns do not outpace inflation.")
            st.session_state.xp += 20
            st.session_state.step = "level_3_cards"
            st.rerun()
        elif ans is not None:
            st.error("Incorrect. Inflation actively erodes real purchasing power over time.")
            if st.button("Continue to Level 3"):
                st.session_state.step = "level_3_cards"
                st.rerun()

# Οθόνη 6: Level 3 - Learning Cards (Investment Principles)
elif st.session_state.step == "level_3_cards":
    st.header("Level 3: Investment Principles & Portfolio Theory")
    st.info("⚖️ **Risk, Return & Diversification**")
    
    st.markdown("""
    * **Equities vs. Bonds:** Equities represent fractional corporate ownership with variable dividends. Bonds are contractual debt instruments with fixed coupon payments and maturity principal return.
    * **The Risk-Return Spectrum:** Higher expected yields inherently demand tolerating greater volatility and higher probability of capital loss.
    * **Portfolio Diversification:** Spreading capital across non-correlated asset classes mitigates unsystematic firm-specific risk.
    """)
    
    if st.button("Proceed to Knowledge Checkpoint (+30 XP)", use_container_width=True):
        st.session_state.xp += 30
        st.session_state.step = "level_3_quiz"
        st.rerun()

# Οθόνη 7: Level 3 - Quiz Checkpoint
elif st.session_state.step == "level_3_quiz":
    st.header("Level 3 Checkpoint: Risk & Diversification")
    st.write("**Question:** What is the primary architectural purpose of diversifying a multi-asset portfolio?")
    
    ans = st.radio(
        "Select the correct answer:",
        [
            "To guarantee complete elimination of all macroeconomic market volatility.",
            "To mitigate unsystematic risk by spreading exposure across multiple non-correlated assets.",
            "To maximize short-term day trading returns."
        ],
        index=None
    )
    
    if st.button("Submit Answer", use_container_width=True):
        if ans == "To mitigate unsystematic risk by spreading exposure across multiple non-correlated assets.":
            st.success("Correct! Diversification mitigates unsystematic risk, protecting against single-firm failure.")
            st.session_state.xp += 20
            st.session_state.step = "level_4_intro"
            st.rerun()
        elif ans is not None:
            st.error("Incorrect. Diversification cannot eliminate systematic market risk, but mitigates unsystematic risk.")
            if st.button("Continue to Level 4"):
                st.session_state.step = "level_4_intro"
                st.rerun()

# Οθόνη 8: Level 4 - Εισαγωγή στα Συμπεριφορικά Διλήμματα
elif st.session_state.step == "level_4_intro":
    st.header("Level 4: Diagnostic Behavioral Bias Screening")
    st.warning("🧠 **Transition to Behavioral Dilemmas**")
    st.write(
        "You have completed foundational financial literacy. Level 4 presents realistic financial dilemmas. "
        "There are no simple 'right or wrong' answers; choose what reflects your genuine instinct."
    )
    if st.button("Begin Diagnostic Dilemmas (+20 XP)", use_container_width=True):
        st.session_state.xp += 20
        st.session_state.step = "dilemma_1"
        st.rerun()

# Οθόνη 9: Dilemma 4.1 - Loss Aversion
elif st.session_state.step == "dilemma_1":
    st.subheader("Module 4.1: Loss Aversion & The Disposition Trap")
    st.caption("Prospect Theory (Kahneman & Tversky, 1979): The pain of loss is twice as intense as equivalent gain pleasure.")
    st.write("**Dilemma:** You bought shares in Company Alpha at €50. The price drops to €35 (-30%) due to structural insolvency. Independent analysts recommend reallocating capital. What do you do?")
    
    options = [
        ("Liquidate immediately at €35, accept the loss, and reallocate into a diversified index fund.", 0, None),
        ("Hold shares temporarily with a strict stop-loss limit to monitor movements.", 1, None),
        ("Refuse to sell until the price recovers to €50 to avoid realizing a loss.", 2, "Preserver")
    ]
    
    if "d1_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d1_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d1_opts], index=None)
    
    if st.button("Confirm Choice (+25 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d1_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 25
            del st.session_state.d1_opts
            st.session_state.step = "dilemma_2"
            st.rerun()

# Οθόνη 10: Dilemma 4.2 - Herd Behavior / FOMO
elif st.session_state.step == "dilemma_2":
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
    
    if st.button("Confirm Choice (+25 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d2_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 25
            del st.session_state.d2_opts
            st.session_state.step = "dilemma_3"
            st.rerun()

# Οθόνη 11: Dilemma 4.3 - Overconfidence
elif st.session_state.step == "dilemma_3":
    st.subheader("Module 4.3: Overconfidence & Illusion of Control")
    st.caption("Overestimating forecasting accuracy and confusing broad bull market momentum with personal skill.")
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
    
    if st.button("Confirm Choice (+25 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d3_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 25
            del st.session_state.d3_opts
            st.session_state.step = "dilemma_4"
            st.rerun()

# Οθόνη 12: Dilemma 4.4 - Present Bias
elif st.session_state.step == "dilemma_4":
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
    
    if st.button("Complete Evaluation (+25 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d4_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            st.session_state.xp += 25
            del st.session_state.d4_opts
            st.session_state.step = "results"
            st.rerun()

# Οθόνη 13: Τελικό Behavioral Scorecard
elif st.session_state.step == "results":
    st.balloons()
    st.title("🏆 Evaluation Complete: Behavioral Scorecard")
    st.write(f"Learner: **{st.session_state.user_name}** | Total XP Earned: **{st.session_state.xp} / 300**")
    
    # Προσδιορισμός προφίλ Pompian
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
    
    # Quantitative Vulnerability Index
    st.metric(label="Vulnerability Score (0–8 pts)", value=f"{score} / 8")
    if score <= 2:
        st.success("🟢 **Low Bias Susceptibility:** Demonstrates strong emotional discipline and objective evaluation.")
    elif score <= 5:
        st.warning("🟡 **Moderate Bias Susceptibility:** Occasional vulnerability to cognitive shortcuts; mindful review recommended.")
    else:
        st.error("🔴 **High Bias Susceptibility:** Elevated emotional sensitivity in financial environments; strict de-biasing nudges required.")
        
    st.markdown("### 🏅 Milestone Badges Earned:")
    st.markdown("- 🥉 **Money Basics Explorer** (Level 1)")
    st.markdown("- 🥈 **Economics Apprentice** (Level 2)")
    st.markdown("- 🥇 **Investing Novice** (Level 3)")
    st.markdown("- 🎖️ **Behavioral Learner** (Level 4)")
    
    if st.button("Restart Experience 🔄", use_container_width=True):
        st.session_state.clear()
        st.rerun()
