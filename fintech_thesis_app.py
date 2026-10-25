import streamlit as st
import random
import sqlite3

# ==========================================
# 1. ΒΑΣΙΚΗ ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ (ΠΡΩΤΗ ΕΝΤΟΛΗ)
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
if "current_level" not in st.session_state:
    st.session_state.current_level = 1
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
# 7. ΟΘΟΝΕΣ ΕΦΑΡΜΟΓΗΣ
# ==========================================

# Οθόνη 1: Welcome / Onboarding
if st.session_state.step == "welcome":
    st.title("🎓 FinTech Behavioral Profiler & Literacy Evaluator")
    st.caption("Master's Thesis Research Prototype | University of Piraeus")
    
    st.markdown("""
    Welcome to this interactive behavioral evaluation environment. This tool benchmarks foundational 
    financial literacy and diagnoses cognitive biases across realistic financial scenarios.
    """)
    
    st.markdown("---")
    st.subheader("📋 Evaluation Structure & Flow")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        * **Level 1:** Financial Foundations (Personal Money Management)
        * **Level 2:** Core Economic Mechanics
        """)
    with col2:
        st.markdown("""
        * **Level 3:** Investment Principles & Portfolio Theory
        * **Level 4:** Diagnostic Behavioral Bias Quizzes
        """)
        
    st.caption("⏱️ **Estimated Duration:** 3–4 minutes | **Target:** 300 Mastery XP")
    st.markdown("---")
    
    user_input = st.text_input(
        "Participant Identifier (Name or ID):", 
        value="", 
        placeholder="e.g., Alex or Participant #01"
    )
    
    st.caption("🔒 *Research Ethics & Privacy:* You may use a pseudonym or ID code. All responses are fully anonymized for academic evaluation purposes.")
    
    if st.button("Start Diagnostic Journey 🚀", use_container_width=True):
        st.session_state.user_name = user_input.strip() if user_input.strip() != "" else "Anonymous Learner"
        st.session_state.step = "level_1_cards"
        st.rerun()

# Οθόνη 2: Level 1 - Theory
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
        st.session_state.pop("l1_status", None)
        st.rerun()

# Οθόνη 3: Level 1 - Quiz Checkpoint (με Feedback & Try Again)
elif st.session_state.step == "level_1_quiz":
    st.caption("Checkpoint 1 of 3 | Financial Foundations")
    st.header("Level 1 Checkpoint: Cash Flow")
    st.write("**Question:** What is the primary function of establishing an emergency fund (reserve)?")
    
    correct_l1 = "To provide a liquid cash cushion covering 3–6 months of essential living expenses during unforeseen crises."
    
    ans = st.radio(
        "Select the correct answer:",
        [
            "To maximize high-risk speculative trading opportunities.",
            correct_l1,
            "To purchase luxury lifestyle items without waiting."
        ],
        index=None,
        key="radio_l1"
    )
    
    if "l1_status" not in st.session_state:
        st.session_state.l1_status = None
        
    if st.session_state.l1_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans is None:
                st.warning("Please choose an answer before submitting.")
            elif ans == correct_l1:
                st.session_state.l1_status = "correct"
                st.session_state.xp += 20
                st.toast("🎉 +20 XP Earned!", icon="✨")
                st.rerun()
            else:
                st.session_state.l1_status = "incorrect"
                st.rerun()
                
    elif st.session_state.l1_status == "correct":
        st.success("✅ **Correct!** Emergency reserves ensure defensive liquidity without relying on high-interest debt or selling investments during downturns.")
        if st.button("Proceed to Level 2 ➔", use_container_width=True):
            st.session_state.pop("l1_status", None)
            st.session_state.step = "level_2_cards"
            st.rerun()
            
    elif st.session_state.l1_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Learning Takeaway:** An emergency fund must never be tied to speculation or consumption. Its primary architectural role is immediate capital preservation and liquidity.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.l1_status = None
            st.rerun()

# Οθόνη 4: Level 2 - Theory
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
        st.session_state.pop("l2_status", None)
        st.rerun()

# Οθόνη 5: Level 2 - Quiz Checkpoint (με Feedback & Try Again)
elif st.session_state.step == "level_2_quiz":
    st.caption("Checkpoint 2 of 3 | Core Economic Mechanics")
    st.header("Level 2 Checkpoint: Inflation & Compounding")
    st.write("**Question:** If annual inflation averages 4% while cash remains stored uninvested at 0% return, what occurs to your capital over time?")
    
    correct_l2 = "The purchasing power decreases, meaning the same nominal money buys fewer goods and services."
    
    ans = st.radio(
        "Select the correct answer:",
        [
            correct_l2,
            "The nominal value of cash automatically increases to match inflation.",
            "Purchasing power remains completely unchanged."
        ],
        index=None,
        key="radio_l2"
    )
    
    if "l2_status" not in st.session_state:
        st.session_state.l2_status = None
        
    if st.session_state.l2_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans is None:
                st.warning("Please choose an answer before submitting.")
            elif ans == correct_l2:
                st.session_state.l2_status = "correct"
                st.session_state.xp += 20
                st.toast("🎉 +20 XP Earned!", icon="✨")
                st.rerun()
            else:
                st.session_state.l2_status = "incorrect"
                st.rerun()
                
    elif st.session_state.l2_status == "correct":
        st.success("✅ **Correct!** Real purchasing power actively deteriorates when investment returns lag behind the rate of inflation.")
        if st.button("Proceed to Level 3 ➔", use_container_width=True):
            st.session_state.pop("l2_status", None)
            st.session_state.step = "level_3_cards"
            st.rerun()
            
    elif st.session_state.l2_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Learning Takeaway:** While nominal balances stay the same (e.g., €100 remains €100), price rises diminish what that money can actually acquire.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.l2_status = None
            st.rerun()

# Οθόνη 6: Level 3 - Theory
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
        st.session_state.pop("l3_status", None)
        st.rerun()

# Οθόνη 7: Level 3 - Quiz Checkpoint (με Feedback & Try Again)
elif st.session_state.step == "level_3_quiz":
    st.caption("Checkpoint 3 of 3 | Portfolio Principles")
    st.header("Level 3 Checkpoint: Risk & Diversification")
    st.write("**Question:** What is the primary architectural purpose of diversifying a multi-asset portfolio?")
    
    correct_l3 = "To mitigate unsystematic risk by spreading exposure across multiple non-correlated assets."
    
    ans = st.radio(
        "Select the correct answer:",
        [
            "To guarantee complete elimination of all macroeconomic market volatility.",
            correct_l3,
            "To maximize short-term day trading returns."
        ],
        index=None,
        key="radio_l3"
    )
    
    if "l3_status" not in st.session_state:
        st.session_state.l3_status = None
        
    if st.session_state.l3_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans is None:
                st.warning("Please choose an answer before submitting.")
            elif ans == correct_l3:
                st.session_state.l3_status = "correct"
                st.session_state.xp += 20
                st.toast("🎉 +20 XP Earned!", icon="✨")
                st.rerun()
            else:
                st.session_state.l3_status = "incorrect"
                st.rerun()
                
    elif st.session_state.l3_status == "correct":
        st.success("✅ **Correct!** Diversification neutralizes unsystematic (company-specific) shocks without necessarily sacrificing expected portfolio yield.")
        if st.button("Proceed to Level 4 (Behavioral Evaluation) ➔", use_container_width=True):
            st.session_state.pop("l3_status", None)
            st.session_state.step = "level_4_intro"
            st.rerun()
            
    elif st.session_state.l3_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Learning Takeaway:** Market-wide (systematic) risk can never be fully diversified away. Diversification specifically shields against the failure of individual companies.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.l3_status = None
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
    st.caption("Dilemma 1 of 4 | Behavioral Diagnosis")
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
    st.caption("Dilemma 3 of 4 | Behavioral Diagnosis")
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
