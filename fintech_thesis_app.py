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
    * **Card 1 — Saving & Budgeting:** Budgeting is planning how every euro is spent instead of wondering where it went. Saving is keeping a portion of your money untouched for the future.
    * **Card 2 — The 50/30/20 Framework:** A practical guideline for your income:
        * **50% Needs:** Essential living expenses (housing, bills, basic food).
        * **30% Wants:** Lifestyle and entertainment choices (eating out, gaming, fashion).
        * **20% Savings:** Money set aside for debt reduction and future security.
    * **Card 3 — Emergency Fund:** A cash safety net covering 3–6 months of essential costs. It shields you from unexpected shocks (e.g., medical costs, broken laptop) without taking expensive loans.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 1.1 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m1_1_quiz"
        st.session_state.pop("m1_1_status", None)
        st.rerun()

elif st.session_state.step == "m1_1_quiz":
    st.caption("Checkpoint 1.1 | Saving & Personal Budgeting")
    st.header("Knowledge Checkpoint 1.1")
    st.write("**Question:** What is the primary function of establishing an emergency fund (reserve)?")
    
    correct = "To provide a liquid cash cushion covering 3–6 months of essential living expenses during unforeseen crises."
    ans = st.radio("Select the correct answer:", [
        "To risk in speculative short-term trading to double capital quickly.",
        correct,
        "To purchase luxury fashion items immediately without waiting."
    ], index=None, key="r_m1_1")
    
    if "m1_1_status" not in st.session_state:
        st.session_state.m1_1_status = None
        
    if st.session_state.m1_1_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m1_1_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 +15 XP Earned!", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m1_1_status = "incorrect"
                st.rerun()
    elif st.session_state.m1_1_status == "correct":
        st.success("✅ **Correct!** Emergency reserves ensure defensive liquidity without relying on high-interest debt during crises.")
        if st.button("Continue to Module 1.2 ➔", use_container_width=True):
            st.session_state.pop("m1_1_status", None)
            st.session_state.step = "m1_2_theory"
            st.rerun()
    elif st.session_state.m1_1_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Emergency reserves are designed solely to cover basic living expenses during sudden crises, not for luxury purchases or speculation.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m1_1_status = None
            st.rerun()

# --- Module 1.2: Debit Cards vs. Credit Cards ---
elif st.session_state.step == "m1_2_theory":
    st.caption("Level 1: Financial Foundations | Module 1.2")
    st.header("Module 1.2: Debit Cards vs. Credit Cards")
    st.info("🎯 **Pedagogical Objective:** Differentiate between self-funded transactional tools and revolving debt instruments.")
    
    st.markdown("""
    * **Card 1 — Debit Cards (Own Funds):** Directly linked to your checking account. Every time you tap, funds are deducted immediately in real time. You cannot spend more than you have (no debt incurred).
    * **Card 2 — Credit Cards (Institutional Borrowing):** When you pay, the bank covers the bill on your behalf. You receive a monthly statement to pay back what you borrowed.
    * **Card 3 — The APR Debt Trap:** If you don't pay the full balance by the due date, credit cards charge extremely high interest rates (Annual Percentage Rate - APR). Revolving credit balances can spiral into severe debt.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 1.2 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m1_2_quiz"
        st.session_state.pop("m1_2_status", None)
        st.rerun()

elif st.session_state.step == "m1_2_quiz":
    st.caption("Checkpoint 1.2 | Debit Cards vs. Credit Cards")
    st.header("Knowledge Checkpoint 1.2")
    st.write("**Question:** What is the fundamental difference when executing a transaction with a credit card compared to a debit card?")
    
    correct = "A credit card involves borrowed capital from an institution that incurs high interest if the statement is not fully repaid."
    ans = st.radio("Select the correct answer:", [
        correct,
        "A debit card borrows money from the bank, while a credit card spends your deposited salary.",
        "Both cards use borrowed funds, but debit cards charge higher monthly maintenance fees."
    ], index=None, key="r_m1_2")
    
    if "m1_2_status" not in st.session_state:
        st.session_state.m1_2_status = None
        
    if st.session_state.m1_2_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m1_2_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 +15 XP Earned!", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m1_2_status = "incorrect"
                st.rerun()
    elif st.session_state.m1_2_status == "correct":
        st.success("✅ **Correct!** Debit cards withdraw your own money immediately; credit cards draw from an institutional line of credit carrying high interest if unpaid.")
        if st.button("Continue to Module 1.3 ➔", use_container_width=True):
            st.session_state.pop("m1_2_status", None)
            st.session_state.step = "m1_3_theory"
            st.rerun()
    elif st.session_state.m1_2_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Credit cards allow short-term borrowing from the bank. If you carry a balance month-to-month, you pay punishing interest rates.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m1_2_status = None
            st.rerun()

# --- Module 1.3: Digital Banking & Payment Security ---
elif st.session_state.step == "m1_3_theory":
    st.caption("Level 1: Financial Foundations | Module 1.3")
    st.header("Module 1.3: Digital Banking & Payment Security")
    st.info("🎯 **Pedagogical Objective:** Develop cybersecurity awareness and defensive digital transaction habits.")
    
    st.markdown("""
    * **Card 1 — Mobile Wallets & The 'Pain of Paying':** Digital wallets (Apple Pay, Google Pay) offer frictionless convenience. However, because you don't physically count cash, behavioral psychology shows we feel less 'pain of paying', making it easier to overspend.
    * **Card 2 — Credential Defense & Phishing:** Banks never ask for your PIN, passwords, or One-Time Passwords (OTPs) via email, SMS, or phone calls. Phishing messages create fake urgency to steal your account access.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 1.3 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m1_3_quiz"
        st.session_state.pop("m1_3_status", None)
        st.rerun()

elif st.session_state.step == "m1_3_quiz":
    st.caption("Checkpoint 1.3 | Digital Banking Security")
    st.header("Knowledge Checkpoint 1.3")
    st.write("**Question:** What is a fundamental security rule when utilizing digital banking and payment cards?")
    
    correct = "Never disclose personal credentials, PINs, or one-time passwords to third parties or unsolicited links."
    ans = st.radio("Select the correct answer:", [
        "Share your PIN with customer service whenever an email marks an account as 'locked'.",
        correct,
        "Write your password down on the back of your payment card for convenience."
    ], index=None, key="r_m1_3")
    
    if "m1_3_status" not in st.session_state:
        st.session_state.m1_3_status = None
        
    if st.session_state.m1_3_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m1_3_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 Level 1 Completed! +15 XP", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m1_3_status = "incorrect"
                st.rerun()
    elif st.session_state.m1_3_status == "correct":
        st.success("✅ **Correct!** Banks will never demand your secret PIN or OTP codes. Guarding your credentials prevents unauthorized takeovers.")
        if st.button("Proceed to Level 2 (Economic Mechanics) ➔", use_container_width=True):
            st.session_state.pop("m1_3_status", None)
            st.session_state.step = "m2_1_theory"
            st.rerun()
    elif st.session_state.m1_3_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Never disclose authentication codes or PINs. Legitimate financial institutions will never solicit this information via links or messages.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m1_3_status = None
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
    * **Card 1 — The Dual Nature of Interest:** 
        * For a **borrower**, interest is the price or compensation cost paid to the lender for using their money.
        * For a **saver/lender**, interest is the reward paid by the bank for depositing money.
    * **Card 2 — Productive vs. Destructive Debt:**
        * **Productive Debt:** Low-cost borrowing that expands your future earning potential or builds assets (e.g., educational loans, a modest home mortgage).
        * **Destructive Debt:** High-interest borrowing used to fund temporary lifestyle consumption (e.g., payday loans, credit cards for clothes/leisure).
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 2.1 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m2_1_quiz"
        st.session_state.pop("m2_1_status", None)
        st.rerun()

elif st.session_state.step == "m2_1_quiz":
    st.caption("Checkpoint 2.1 | Interest Rates & Borrowing")
    st.header("Knowledge Checkpoint 2.1")
    st.write("**Question:** In the context of personal finance, what does the interest rate represent to a borrower?")
    
    correct = "The periodic compensation cost paid to a lending institution for utilizing borrowed funds."
    ans = st.radio("Select the correct answer:", [
        "A bonus paid by the bank to the borrower as a loyalty reward.",
        correct,
        "A fixed government tax dedicated solely to road maintenance."
    ], index=None, key="r_m2_1")
    
    if "m2_1_status" not in st.session_state:
        st.session_state.m2_1_status = None
        
    if st.session_state.m2_1_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m2_1_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 +15 XP Earned!", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m2_1_status = "incorrect"
                st.rerun()
    elif st.session_state.m2_1_status == "correct":
        st.success("✅ **Correct!** For borrowers, interest is the cost of renting capital. Minimizing high-interest borrowing protects personal wealth.")
        if st.button("Continue to Module 2.2 ➔", use_container_width=True):
            st.session_state.pop("m2_1_status", None)
            st.session_state.step = "m2_2_theory"
            st.rerun()
    elif st.session_state.m2_1_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Interest is neither a gift nor a general tax; it is the direct fee charged by lenders for granting credit.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m2_1_status = None
            st.rerun()

# --- Module 2.2: The Mechanics of Inflation ---
elif st.session_state.step == "m2_2_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.2")
    st.header("Module 2.2: The Mechanics of Inflation")
    st.info("🎯 **Pedagogical Objective:** Analyze purchasing power erosion and the divergence between nominal and real values.")
    
    st.markdown("""
    * **Card 1 — General Price Increases (CPI):** Inflation measures how prices across goods and services rise over time, tracked through the Consumer Price Index (CPI).
    * **Card 2 — Purchasing Power Erosion:** If your money sits at 0% return while prices rise, its nominal face value stays identical (a €100 note is still €100), but its **real purchasing power** shrinks.
    * **Card 3 — The €100 Simulation:** 
        * At a modest **4% annual inflation**, a basket of goods costing **€100 today** will cost **€104 in 1 year** and approximately **€121.66 in 5 years**.
        * Your uninvested €100 note will buy significantly fewer goods as time progresses.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 2.2 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m2_2_quiz"
        st.session_state.pop("m2_2_status", None)
        st.rerun()

elif st.session_state.step == "m2_2_quiz":
    st.caption("Checkpoint 2.2 | Mechanics of Inflation")
    st.header("Knowledge Checkpoint 2.2")
    st.write("**Question:** If annual inflation averages 4% while cash remains stored uninvested at 0% return, what occurs to your capital over time?")
    
    correct = "The purchasing power decreases, meaning the same nominal money buys fewer products."
    ans = st.radio("Select the correct answer:", [
        correct,
        "The nominal cash automatically increases by 4% to balance purchasing power.",
        "Purchasing power remains completely unaffected because physical banknotes do not physically shrink."
    ], index=None, key="r_m2_2")
    
    if "m2_2_status" not in st.session_state:
        st.session_state.m2_2_status = None
        
    if st.session_state.m2_2_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m2_2_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 +15 XP Earned!", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m2_2_status = "incorrect"
                st.rerun()
    elif st.session_state.m2_2_status == "correct":
        st.success("✅ **Correct!** Inflation quietly erodes what nominal money can actually buy in the real economy.")
        if st.button("Continue to Module 2.3 ➔", use_container_width=True):
            st.session_state.pop("m2_2_status", None)
            st.session_state.step = "m2_3_theory"
            st.rerun()
    elif st.session_state.m2_2_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Even though nominal cash figures stay constant, rising prices mean cash buys less over time (loss of purchasing power).")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m2_2_status = None
            st.rerun()

# --- Module 2.3: Compounding – Exponential Wealth Creation ---
elif st.session_state.step == "m2_3_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.3")
    st.header("Module 2.3: Compounding – Exponential Wealth Creation")
    st.info("🎯 **Pedagogical Objective:** Understand exponential growth generated by continuous reinvestment of accumulated returns.")
    
    st.markdown("""
    * **Card 1 — Simple vs. Compound Interest:** 
        * **Simple Interest:** You only earn returns on your original principal deposit.
        * **Compound Interest:** You earn return on your principal **plus on all previously earned returns**. This is 'earning return on prior return'.
    * **Card 2 — The Early Start Trajectory:** Over long horizons (10, 20, 30 years), compounding creates a steep hockey-stick growth curve. Starting disciplined investing at age 20 rather than 35 produces dramatically higher wealth with far less personal capital deployed.
    """)
    st.caption("📚 *Institutional Reference:* Philippas (2022); Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 2.3 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m2_3_quiz"
        st.session_state.pop("m2_3_status", None)
        st.rerun()

elif st.session_state.step == "m2_3_quiz":
    st.caption("Checkpoint 2.3 | Exponential Compounding")
    st.header("Knowledge Checkpoint 2.3")
    st.write("**Question:** Why is compound interest considered one of the most powerful mechanisms in personal wealth accumulation?")
    
    correct = "It generates exponential growth by continuously earning returns on both the principal and previously accumulated interest."
    ans = st.radio("Select the correct answer:", [
        "It eliminates all forms of financial taxes by legal exemption.",
        correct,
        "It guarantees immediate doubling of invested capital within 24 hours."
    ], index=None, key="r_m2_3")
    
    if "m2_3_status" not in st.session_state:
        st.session_state.m2_3_status = None
        
    if st.session_state.m2_3_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m2_3_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 Level 2 Completed! +15 XP", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m2_3_status = "incorrect"
                st.rerun()
    elif st.session_state.m2_3_status == "correct":
        st.success("✅ **Correct!** Reinvesting accumulated returns creates a compounding snowball effect over extended investment horizons.")
        if st.button("Proceed to Level 3 (Investment Principles) ➔", use_container_width=True):
            st.session_state.pop("m2_3_status", None)
            st.session_state.step = "m3_1_theory"
            st.rerun()
    elif st.session_state.m2_3_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Compounding powers exponential growth because returns generate their own returns when left invested over time.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m2_3_status = None
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
    * **Card 1 — Equity Shares (Corporate Ownership):** Buying a share means purchasing a fractional slice of ownership in a business. As a shareholder, you participate in potential corporate growth and may receive variable profit distributions (dividends). However, share values fluctuate daily and capital can be lost.
    * **Card 2 — Fixed-Income Bonds (Creditor Loans):** A bond is a contractual debt certificate. When you buy a bond, you lend money to an institution or government. In return, the issuer promises to pay you regular fixed interest (coupon payments) and return the full principal (face value) upon maturity.
    """)
    st.caption("📚 *Institutional Reference:* Hellenic Capital Market Commission & Financial Literacy Institute (2026); Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 3.1 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m3_1_quiz"
        st.session_state.pop("m3_1_status", None)
        st.rerun()

elif st.session_state.step == "m3_1_quiz":
    st.caption("Checkpoint 3.1 | Equities vs. Bonds")
    st.header("Knowledge Checkpoint 3.1")
    st.write("**Question:** What core legal and economic distinction separates a stock from a government bond?")
    
    correct = "Stocks confer fractional ownership in a firm, whereas bonds are contractual debt instruments paying fixed interest."
    ans = st.radio("Select the correct answer:", [
        "Stocks guarantee a legally fixed interest repayment, whereas bonds represent voting shares in management.",
        correct,
        "There is no distinction; both terms represent identical financial assets."
    ], index=None, key="r_m3_1")
    
    if "m3_1_status" not in st.session_state:
        st.session_state.m3_1_status = None
        
    if st.session_state.m3_1_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m3_1_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 +15 XP Earned!", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m3_1_status = "incorrect"
                st.rerun()
    elif st.session_state.m3_1_status == "correct":
        st.success("✅ **Correct!** Equity provides ownership rights and variable upside, while bonds constitute debt contracts paying predetermined coupons.")
        if st.button("Continue to Module 3.2 ➔", use_container_width=True):
            st.session_state.pop("m3_1_status", None)
            st.session_state.step = "m3_2_theory"
            st.rerun()
    elif st.session_state.m3_1_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Shares represent company ownership (equity), while bonds represent contractual loans provided to issuers (debt).")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m3_1_status = None
            st.rerun()

# --- Module 3.2: The Risk-Return Spectrum ---
elif st.session_state.step == "m3_2_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.2")
    st.header("Module 3.2: The Risk-Return Spectrum")
    st.info("🎯 **Pedagogical Objective:** Master the foundational axiom linking potential investment yields to volatility and downside risk.")
    
    st.markdown("""
    * **Card 1 — Conceptualizing Financial Risk:** Investment risk is not just 'danger'—it is the statistical uncertainty regarding future outcomes, including the probability of capital loss or underperformance.
    * **Card 2 — The Trade-Off Axiom:** In efficient markets, higher expected long-term yields cannot be achieved without accepting greater price fluctuations (volatility) and deeper downside drawdown risk. Anyone offering 'high guaranteed returns with zero risk' is describing an impossible mathematical promise or a fraud.
    """)
    st.caption("📚 *Institutional Reference:* Hellenic Capital Market Commission & Financial Literacy Institute (2026)")
    
    if st.button("Proceed to Checkpoint 3.2 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m3_2_quiz"
        st.session_state.pop("m3_2_status", None)
        st.rerun()

elif st.session_state.step == "m3_2_quiz":
    st.caption("Checkpoint 3.2 | Risk-Return Trade-Off")
    st.header("Knowledge Checkpoint 3.2")
    st.write("**Question:** According to the foundational Risk-Return trade-off principle in financial economics:")
    
    correct = "Achieving higher long-term expected returns requires an investor to tolerate greater volatility and probability of capital loss."
    ans = st.radio("Select the correct answer:", [
        "High returns can be guaranteed indefinitely without any risk of capital decline.",
        correct,
        "Low-risk assets systematically generate higher compound yields than volatile equities over decades."
    ], index=None, key="r_m3_2")
    
    if "m3_2_status" not in st.session_state:
        st.session_state.m3_2_status = None
        
    if st.session_state.m3_2_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m3_2_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 +15 XP Earned!", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m3_2_status = "incorrect"
                st.rerun()
    elif st.session_state.m3_2_status == "correct":
        st.success("✅ **Correct!** Risk and return are intrinsically linked: superior potential return demands accepting higher short-term uncertainty.")
        if st.button("Continue to Module 3.3 ➔", use_container_width=True):
            st.session_state.pop("m3_2_status", None)
            st.session_state.step = "m3_3_theory"
            st.rerun()
    elif st.session_state.m3_2_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Higher returns are the economic compensation for enduring greater downside volatility and capital risk.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m3_2_status = None
            st.rerun()

# --- Module 3.3: Portfolio Diversification & Asset Allocation ---
elif st.session_state.step == "m3_3_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.3")
    st.header("Module 3.3: Portfolio Diversification & Asset Allocation")
    st.info("🎯 **Pedagogical Objective:** Understand unsystematic risk mitigation through balanced multi-asset allocation.")
    
    st.markdown("""
    * **Card 1 — Don't Put All Eggs in One Basket:** If you place 100% of your savings into a single company and it collapses, your entire capital is wiped out. Spreading money across diverse firms prevents single-firm ruin.
    * **Card 2 — Asset Class Allocation:** Combining assets that react differently to economic events (e.g., equities, government bonds, cash reserves) cushions overall portfolio stability. While broad market shocks cannot be eliminated, company-specific (unsystematic) failure is effectively mitigated.
    """)
    st.caption("📚 *Institutional Reference:* Hellenic Capital Market Commission & Financial Literacy Institute (2026); Philippas (2022)")
    
    if st.button("Proceed to Checkpoint 3.3 (+10 XP)", use_container_width=True):
        st.session_state.xp += 10
        st.session_state.step = "m3_3_quiz"
        st.session_state.pop("m3_3_status", None)
        st.rerun()

elif st.session_state.step == "m3_3_quiz":
    st.caption("Checkpoint 3.3 | Portfolio Diversification")
    st.header("Knowledge Checkpoint 3.3")
    st.write("**Question:** What is the primary architectural purpose of diversifying a multi-asset portfolio?")
    
    correct = "To mitigate unsystematic risk by spreading exposure across multiple non-correlated assets, preventing catastrophic single-asset failure."
    ans = st.radio("Select the correct answer:", [
        "To guarantee that broad global market declines will never temporarily decrease asset values.",
        correct,
        "To achieve maximum leverage for high-frequency day trading."
    ], index=None, key="r_m3_3")
    
    if "m3_3_status" not in st.session_state:
        st.session_state.m3_3_status = None
        
    if st.session_state.m3_3_status is None:
        if st.button("Submit Answer", use_container_width=True):
            if ans == correct:
                st.session_state.m3_3_status = "correct"
                st.session_state.xp += 15
                st.toast("🎉 Level 3 Completed! +15 XP", icon="✨")
                st.rerun()
            elif ans is not None:
                st.session_state.m3_3_status = "incorrect"
                st.rerun()
    elif st.session_state.m3_3_status == "correct":
        st.success("✅ **Correct!** Diversification neutralizes unsystematic (single-company) vulnerability without sacrificing expected risk-adjusted returns.")
        if st.button("Proceed to Level 4 (Behavioral Evaluation) ➔", use_container_width=True):
            st.session_state.pop("m3_3_status", None)
            st.session_state.step = "level_4_intro"
            st.rerun()
    elif st.session_state.m3_3_status == "incorrect":
        st.error("❌ **Incorrect Answer.**")
        st.info("💡 **Takeaway:** Diversification shields wealth against company-specific defaults, even though macro market cycles affect overall assets.")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.m3_3_status = None
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
