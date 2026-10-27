import streamlit as st
import random
import sqlite3
import pandas as pd
import time

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
# 3. ΡΥΘΜΙΣΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ (SQLITE)
# ==========================================
def init_db():
    conn = sqlite3.connect("quiz_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            total_xp INTEGER,
            completion_time_minutes REAL,
            vulnerability_score INTEGER,
            dominant_archetype TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(name, xp, minutes, score, archetype):
    conn = sqlite3.connect("quiz_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_results (user_name, total_xp, completion_time_minutes, vulnerability_score, dominant_archetype)
        VALUES (?, ?, ?, ?, ?)
    """, (name, xp, minutes, score, archetype))
    conn.commit()
    conn.close()

def get_all_results():
    conn = sqlite3.connect("quiz_data.db")
    df = pd.read_sql_query("SELECT id, user_name, total_xp, completion_time_minutes, vulnerability_score, dominant_archetype FROM user_results", conn)
    conn.close()
    return df

init_db()

# ==========================================
# 4. PIN ACCESS GATEWAY & ADMIN PANEL
# ==========================================
USER_PIN = "9218"
ADMIN_PIN = "1453"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

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
            label_visibility="collapsed",
            key="pin_field"
        )
    with col2:
        submit_btn = st.button("Enter ➔", use_container_width=True)
        
    if submit_btn:
        if pin_input == USER_PIN:
            st.session_state.authenticated = True
            st.session_state.is_admin = False
            st.rerun()
        elif pin_input == ADMIN_PIN:
            st.session_state.authenticated = True
            st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("❌ Invalid PIN. Please check your credentials.")
            
    st.stop()

# --- Admin Dashboard View ---
if st.session_state.is_admin:
    st.title("📊 Researcher Admin Dashboard")
    st.caption("Database Overview | University of Piraeus M.Sc. Research")
    
    df_results = get_all_results()
    st.metric(label="Total Recorded Submissions", value=len(df_results))
    
    if not df_results.empty:
        st.dataframe(df_results, use_container_width=True)
        
        csv_data = df_results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results as CSV (Excel)",
            data=csv_data,
            file_name="participant_results.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No participant records found in the database yet.")
        
    if st.button("Exit Admin Mode 🚪", use_container_width=True):
        st.session_state.clear()
        st.session_state.authenticated = False
        st.session_state.is_admin = False
        st.session_state.step = "welcome"
        st.rerun()
        
    st.stop()

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

if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = set()

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
        
    st.caption("⏱️ **Estimated Duration:** 12–15 minutes | **Target:** 300 Mastery XP")
    st.markdown("---")
    
    user_input = st.text_input(
        "Participant Identifier (Name or ID):", 
        value="", 
        placeholder="e.g., Alex or Participant #01"
    )
    
    st.caption("🔒 *Research Ethics & Privacy:* You may use a pseudonym or ID code. All responses are fully anonymized for academic evaluation purposes.")
    
    if st.button("Start Diagnostic Journey 🚀", use_container_width=True):
        st.session_state.user_name = user_input.strip() if user_input.strip() != "" else "Anonymous Learner"
        st.session_state.start_time = time.time()  # <-- Καταγραφή ώρας έναρξης
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
    * **Saving & Budgeting Principles:** Budgeting is planning where each euro goes rather than wondering where it disappeared. Saving represents capital preserved untouched for future security.
    * **The 50/30/20 Framework:** Allocate net income systematically:
        * **50% Needs:** Essential expenditures (housing, bills, groceries).
        * **30% Wants:** Discretionary lifestyle choices (dining out, entertainment, hobbies).
        * **20% Savings:** Dedicated capital for debt clearance and long-term wealth building.
    * **Emergency Reserve (Emergency Fund):** A dedicated liquid cushion equal to 3–6 months of essential living costs. It prevents forced borrowing or high-interest debt during sudden crises.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "welcome"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 1.1 (+10 XP)", use_container_width=True):
            if "m1_1_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m1_1_theory")
            st.session_state.step = "m1_1_quiz"
            st.session_state.pop("m1_1_status", None)
            st.rerun()

elif st.session_state.step == "m1_1_quiz":
    st.caption("Checkpoint 1.1 | Saving & Personal Budgeting")
    st.header("Knowledge Checkpoint 1.1")
    st.write("**Question:** What is the primary function of establishing an emergency fund (reserve)?")
    
    correct = "To provide a cash cushion covering 3–6 months of basic living costs during unexpected emergencies."
    ans = st.radio("Select the correct answer:", [
        "To gamble on high-risk trading games to double money quickly.",
        correct,
        "To purchase luxury fashion items immediately without waiting."
    ], index=None, key="r_m1_1")
    
    if "m1_1_status" not in st.session_state:
        st.session_state.m1_1_status = None
        
    if st.session_state.m1_1_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m1_1_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m1_1_status = "correct"
                    if "m1_1_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m1_1_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m1_1_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m1_1_status = None
                st.rerun()

# --- Module 1.2: Debit Cards vs. Credit Cards ---
elif st.session_state.step == "m1_2_theory":
    st.caption("Level 1: Financial Foundations | Module 1.2")
    st.header("Module 1.2: Debit Cards vs. Credit Cards")
    st.info("🎯 **Pedagogical Objective:** Understand the difference between spending your own money and using borrowed bank money.")
    
    st.markdown("""
    * **Debit Cards (Direct Account Deduction):** Linked directly to your bank account. When you pay, **your own money is taken out immediately**, so you never owe anything to the bank.
    * **Credit Cards (Short-Term Institutional Debt):** The bank pays the shop for you, giving you **borrowed money**. At the end of the month, you receive a bill to pay the bank back.
    * **Annual Percentage Rate (APR Risk):** If you don't repay the full credit card bill on time, the bank charges you very high extra fees (interest). What started as an easy buy can quickly turn into dangerous debt.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m1_1_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 1.2 (+10 XP)", use_container_width=True):
            if "m1_2_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m1_2_theory")
            st.session_state.step = "m1_2_quiz"
            st.session_state.pop("m1_2_status", None)
            st.rerun()

elif st.session_state.step == "m1_2_quiz":
    st.caption("Checkpoint 1.2 | Debit Cards vs. Credit Cards")
    st.header("Knowledge Checkpoint 1.2")
    st.write("**Question:** What is the fundamental difference when executing a transaction with a credit card compared to a debit card?")
    
    correct = "A credit card uses money borrowed from the bank that charges high interest if the monthly bill is not repaid in full."
    ans = st.radio("Select the correct answer:", [
        correct,
        "A debit card borrows money from the bank, while a credit card spends your own money.",
        "Both cards use borrowed money, but debit cards charge extra fees for each purchase."
    ], index=None, key="r_m1_2")
    
    if "m1_2_status" not in st.session_state:
        st.session_state.m1_2_status = None
        
    if st.session_state.m1_2_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m1_2_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m1_2_status = "correct"
                    if "m1_2_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m1_2_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m1_2_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m1_2_status = None
                st.rerun()

# --- Module 1.3: Digital Banking & Payment Security ---
elif st.session_state.step == "m1_3_theory":
    st.caption("Level 1: Financial Foundations | Module 1.3")
    st.header("Module 1.3: Digital Banking & Payment Security")
    st.info("🎯 **Pedagogical Objective:** Learn how to pay safely online and protect your digital money.")
    
    st.markdown("""
    * **Mobile Wallets & The 'Pain of Paying':** Tapping your phone (Apple Pay, Google Pay) feels so effortless that you barely notice you are spending real money. Without physically counting cash, it becomes much easier to overspend.
    * **Credential Confidentiality & Phishing Defense:** Banks will **never** ask for your secret PIN, passwords, or SMS verification codes (OTPs) through text messages, emails, or strange links. Keep your login details strictly private.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m1_2_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 1.3 (+10 XP)", use_container_width=True):
            if "m1_3_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m1_3_theory")
            st.session_state.step = "m1_3_quiz"
            st.session_state.pop("m1_3_status", None)
            st.rerun()

elif st.session_state.step == "m1_3_quiz":
    st.caption("Checkpoint 1.3 | Digital Banking Security")
    st.header("Knowledge Checkpoint 1.3")
    st.write("**Question:** What is a fundamental security rule when utilizing digital banking and payment cards?")
    
    correct = "Never share your private passwords, PINs, or one-time verification codes with anyone or through suspicious links."
    ans = st.radio("Select the correct answer:", [
        "Share your PIN with customer support whenever an email says your account is locked.",
        correct,
        "Write your secret password down on the back of your bank card for convenience."
    ], index=None, key="r_m1_3")
    
    if "m1_3_status" not in st.session_state:
        st.session_state.m1_3_status = None
        
    if st.session_state.m1_3_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m1_3_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m1_3_status = "correct"
                    if "m1_3_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m1_3_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m1_3_theory"
                st.rerun()
        with col_r:
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
    st.info("🎯 **Pedagogical Objective:** Understand how interest works: as an extra fee when you borrow, and as a reward when you save.")
    
    st.markdown("""
    * **The Dual Nature of Interest:** 
        * For a **borrower**: Interest is the **extra fee you pay** to the bank for letting you use their money.
        * For a **saver/lender**: Interest is the **reward the bank pays you** for keeping your savings with them.
    * **Productive vs. Destructive Debt:**
        * **Productive Debt:** Affordable borrowing to invest in your future, like studying or buying a home (things that build value over time).
        * **Destructive Debt:** High-interest borrowing for things that lose value right away, like clothes or gadgets you cannot afford (e.g., unpaid credit card balances).
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m1_3_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 2.1 (+10 XP)", use_container_width=True):
            if "m2_1_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m2_1_theory")
            st.session_state.step = "m2_1_quiz"
            st.session_state.pop("m2_1_status", None)
            st.rerun()

elif st.session_state.step == "m2_1_quiz":
    st.caption("Checkpoint 2.1 | Interest Rates & Borrowing")
    st.header("Knowledge Checkpoint 2.1")
    st.write("**Question:** In the context of personal finance, what does the interest rate represent to a borrower?")
    
    correct = "The extra fee you pay to the bank for using their borrowed money."
    ans = st.radio("Select the correct answer:", [
        "A cash bonus paid by the bank to the borrower as a gift.",
        correct,
        "A mandatory government tax used only for road repairs."
    ], index=None, key="r_m2_1")
    
    if "m2_1_status" not in st.session_state:
        st.session_state.m2_1_status = None
        
    if st.session_state.m2_1_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m2_1_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m2_1_status = "correct"
                    if "m2_1_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m2_1_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m2_1_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m2_1_status = None
                st.rerun()

# --- Module 2.2: The Mechanics of Inflation ---
elif st.session_state.step == "m2_2_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.2")
    st.header("Module 2.2: The Mechanics of Inflation")
    st.info("🎯 **Pedagogical Objective:** Understand how rising prices quietly reduce what your money can actually buy over time.")
    
    st.markdown("""
    * **Consumer Price Index (CPI):** Inflation means prices of everyday goods (food, clothes, tickets) rise over time. Economists measure this price increase using a benchmark called the **Consumer Price Index (CPI)**.
    * **Purchasing Power Erosion:** If you keep a €10 note sitting in a drawer at 0% return, the note itself still says "€10", but its **purchasing power** shrinks. If a pizza costs €10 today, in a couple of years the same pizza might cost €12, so your €10 won't be enough to buy it anymore.
    * **The €100 Capital Simulation:** 
        * If inflation runs at **4% per year**, a basket of snacks or clothes costing **€100 today** will cost **€104 in 1 year** and about **€122 in 5 years**.
        * Storing cash idle without investing it means it gradually buys fewer and fewer things.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m2_1_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 2.2 (+10 XP)", use_container_width=True):
            if "m2_2_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m2_2_theory")
            st.session_state.step = "m2_2_quiz"
            st.session_state.pop("m2_2_status", None)
            st.rerun()

elif st.session_state.step == "m2_2_quiz":
    st.caption("Checkpoint 2.2 | Mechanics of Inflation")
    st.header("Knowledge Checkpoint 2.2")
    st.write("**Question:** If annual inflation averages 4% while cash remains stored uninvested at 0% return, what occurs to your capital over time?")
    
    correct = "Its purchasing power drops, meaning the exact same money buys fewer products in the future."
    ans = st.radio("Select the correct answer:", [
        correct,
        "The cash in your wallet automatically grows by 4% to match rising store prices.",
        "Purchasing power stays exactly identical because the number printed on the banknote does not change."
    ], index=None, key="r_m2_2")
    
    if "m2_2_status" not in st.session_state:
        st.session_state.m2_2_status = None
        
    if st.session_state.m2_2_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m2_2_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m2_2_status = "correct"
                    if "m2_2_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m2_2_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m2_2_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m2_2_status = None
                st.rerun()

# --- Module 2.3: Compounding – Exponential Wealth Creation ---
elif st.session_state.step == "m2_3_theory":
    st.caption("Level 2: Core Economic Mechanics | Module 2.3")
    st.header("Module 2.3: Compounding – Exponential Wealth Creation")
    st.info("🎯 **Pedagogical Objective:** Understand how reinvesting your profits makes your money grow faster and faster over time (snowball effect).")
    
    st.markdown("""
    * **Simple vs. Compound Interest Mechanics:** 
        * **Simple Interest:** You only earn profit on the original money you put in.
        * **Compound Interest:** You earn profit on your original money **plus on all previous profits you leave invested** ("making your profits earn their own profits").
    * **The Time Horizon Trajectory:** Leaving your money invested over long periods (10–30 years) creates massive growth. Starting at age 18 instead of 35 allows this snowball to grow dramatically bigger with much less effort.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m2_2_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 2.3 (+10 XP)", use_container_width=True):
            if "m2_3_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m2_3_theory")
            st.session_state.step = "m2_3_quiz"
            st.session_state.pop("m2_3_status", None)
            st.rerun()

elif st.session_state.step == "m2_3_quiz":
    st.caption("Checkpoint 2.3 | Exponential Compounding")
    st.header("Knowledge Checkpoint 2.3")
    st.write("**Question:** Why is compound interest considered one of the most powerful mechanisms in personal wealth accumulation?")
    
    correct = "It creates rapid exponential growth by earning returns on both your starting money and previously earned interest."
    ans = st.radio("Select the correct answer:", [
        "It legally eliminates all types of income and government taxes forever.",
        correct,
        "It promises to instantly double any investment within 24 hours guaranteed."
    ], index=None, key="r_m2_3")
    
    if "m2_3_status" not in st.session_state:
        st.session_state.m2_3_status = None
        
    if st.session_state.m2_3_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m2_3_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m2_3_status = "correct"
                    if "m2_3_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m2_3_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m2_3_theory"
                st.rerun()
        with col_r:
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
    st.info("🎯 **Pedagogical Objective:** Understand the difference between owning a piece of a company (stocks) and lending money for interest (bonds).")
    
    st.markdown("""
    * **Equity Shares (Corporate Ownership):** Buying a stock means buying a tiny slice of ownership in a business (like Apple or Sony). If the company grows and makes profits, your share can become worth much more (and you may get cash rewards called dividends). But if the company struggles, share prices can fall and you risk losing money.
    * **Fixed-Income Bonds (Debt Obligations):** A bond is an official loan certificate. Instead of buying ownership, you lend your money to a government or a large company. In return, they officially promise to pay you regular interest and return your full money back on a set date.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m2_3_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 3.1 (+10 XP)", use_container_width=True):
            if "m3_1_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m3_1_theory")
            st.session_state.step = "m3_1_quiz"
            st.session_state.pop("m3_1_status", None)
            st.rerun()

elif st.session_state.step == "m3_1_quiz":
    st.caption("Checkpoint 3.1 | Equities vs. Bonds")
    st.header("Knowledge Checkpoint 3.1")
    st.write("**Question:** What core legal and economic distinction separates a stock from a government bond?")
    
    correct = "Stocks give you actual partial ownership in a company, whereas bonds are loans that pay you fixed interest."
    ans = st.radio("Select the correct answer:", [
        "Stocks guarantee a legally fixed payout every year, while bonds give you voting power to run the company.",
        correct,
        "There is no distinction; stocks and bonds are just two different names for the exact same asset."
    ], index=None, key="r_m3_1")
    
    if "m3_1_status" not in st.session_state:
        st.session_state.m3_1_status = None
        
    if st.session_state.m3_1_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m3_1_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m3_1_status = "correct"
                    if "m3_1_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m3_1_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m3_1_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m3_1_status = None
                st.rerun()

# --- Module 3.2: The Risk-Return Spectrum ---
elif st.session_state.step == "m3_2_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.2")
    st.header("Module 3.2: The Risk-Return Spectrum")
    st.info("🎯 **Pedagogical Objective:** Learn why aiming for higher profits always means accepting bigger ups and downs (and risk of loss).")
    
    st.markdown("""
    * **Conceptualizing Financial Risk:** In investing, risk simply means uncertainty. It is the chance that an investment's value will jump up and down, and that you might end up with less money than you started with.
    * **The Trade-Off Axiom:** Higher potential profits always go hand-in-hand with higher risk. If an investment can make you a lot of money quickly, it can also lose a lot just as fast. Anyone promising 'huge guaranteed profits with zero risk' is pitching an unrealistic claim.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m3_1_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 3.2 (+10 XP)", use_container_width=True):
            if "m3_2_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m3_2_theory")
            st.session_state.step = "m3_2_quiz"
            st.session_state.pop("m3_2_status", None)
            st.rerun()

elif st.session_state.step == "m3_2_quiz":
    st.caption("Checkpoint 3.2 | Risk-Return Trade-Off")
    st.header("Knowledge Checkpoint 3.2")
    st.write("**Question:** According to the foundational Risk-Return trade-off principle in financial economics:")
    
    correct = "Aiming for higher potential returns means you must accept bigger price swings and a greater chance of losing money."
    ans = st.radio("Select the correct answer:", [
        "Huge profits can easily be guaranteed forever without any danger of losing your starting money.",
        correct,
        "Super safe investments always grow faster and earn more money than stocks over long periods."
    ], index=None, key="r_m3_2")
    
    if "m3_2_status" not in st.session_state:
        st.session_state.m3_2_status = None
        
    if st.session_state.m3_2_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m3_2_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m3_2_status = "correct"
                    if "m3_2_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m3_2_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m3_2_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m3_2_status = None
                st.rerun()

# --- Module 3.3: Portfolio Diversification & Asset Allocation ---
elif st.session_state.step == "m3_3_theory":
    st.caption("Level 3: Investment Principles & Portfolio Theory | Module 3.3")
    st.header("Module 3.3: Portfolio Diversification & Asset Allocation")
    st.info("🎯 **Pedagogical Objective:** Learn why spreading your money across different investments protects you from losing everything (don't put all your eggs in one basket).")
    
    st.markdown("""
    * **The Multi-Asset Principle:** Putting 100% of your money into a single company is very dangerous. If that company goes bankrupt, you lose all your savings. Spreading your cash across different investments protects your money if one goes wrong.
    * **Unsystematic Risk Mitigation:** By mixing different types of investments (like company stocks, government bonds, and cash), bad news in one area won't destroy your whole balance. While markets will always have ups and downs, you completely avoid total ruin from a single company failure.
    """)
    
    col_b, col_n = st.columns([1, 2])
    with col_b:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.step = "m3_2_quiz"
            st.rerun()
    with col_n:
        if st.button("Proceed to Checkpoint 3.3 (+10 XP)", use_container_width=True):
            if "m3_3_theory" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("m3_3_theory")
            st.session_state.step = "m3_3_quiz"
            st.session_state.pop("m3_3_status", None)
            st.rerun()

elif st.session_state.step == "m3_3_quiz":
    st.caption("Checkpoint 3.3 | Portfolio Diversification")
    st.header("Knowledge Checkpoint 3.3")
    st.write("**Question:** What is the primary architectural purpose of diversifying a multi-asset portfolio?")
    
    correct = "To spread your money across different investments so that a failure in one asset will not wipe out your whole portfolio."
    ans = st.radio("Select the correct answer:", [
        "To guarantee that market prices will never drop even temporarily during global crises.",
        correct,
        "To borrow the maximum possible money for risky day-trading."
    ], index=None, key="r_m3_3")
    
    if "m3_3_status" not in st.session_state:
        st.session_state.m3_3_status = None
        
    if st.session_state.m3_3_status is None:
        col_b, col_s = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m3_3_theory"
                st.rerun()
        with col_s:
            if st.button("Submit Answer", use_container_width=True):
                if ans == correct:
                    st.session_state.m3_3_status = "correct"
                    if "m3_3_quiz" not in st.session_state.completed_steps:
                        st.session_state.xp += 15
                        st.session_state.completed_steps.add("m3_3_quiz")
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
        col_b, col_r = st.columns([1, 2])
        with col_b:
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.step = "m3_3_theory"
                st.rerun()
        with col_r:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.m3_3_status = None
                st.rerun()

# ==============================================================================
# LEVEL 4: Diagnostic Behavioral Bias Screening (ΜΟΝΟΣΗΜΑΝΤΗ ΡΟΗ - ΧΩΡΙΣ BACK)
# ==============================================================================

elif st.session_state.step == "level_4_intro":
    st.header("Level 4: Diagnostic Behavioral Bias Screening")
    st.warning("🧠 **Transition to Behavioral Dilemmas**")
    st.write(
        "Congratulations on completing the financial literacy curriculum! Level 4 explores how human emotions and psychological traps influence our money decisions. "
        "Before each dilemma, you will see a brief Awareness Card explaining the bias. Then, you will face a real-world scenario. "
        "There are no simple 'right or wrong' answers here — select what truly reflects your personal reaction."
    )
    if st.button("Begin Behavioral Exploration (+15 XP)", use_container_width=True):
        if "l4_intro" not in st.session_state.completed_steps:
            st.session_state.xp += 15
            st.session_state.completed_steps.add("l4_intro")
        st.session_state.step = "dilemma_1_theory"
        st.rerun()

# --- Module 4.1: Loss Aversion & The Disposition Trap ---
elif st.session_state.step == "dilemma_1_theory":
    st.caption("Level 4: Behavioral Diagnosis | Module 4.1 Awareness")
    st.subheader("Module 4.1: Loss Aversion & The Disposition Trap")
    st.info("🎯 **Behavioral Insight:** Recognize why the pain of admitting a financial loss often leads to much bigger damage.")
    
    st.markdown("""
    * **Loss Aversion:** Psychological research shows that **losing €50 hurts twice as much as the joy of winning €50**. We hate losing so much that we often make irrational choices just to avoid admitting it.
    * **The Disposition Trap:** When an investment falls sharply because the company is failing, investors often stubbornly refuse to sell. They tell themselves *"I haven't lost until I sell,"* hoping it climbs back to their buy price. This emotional freeze often causes catastrophic losses.
    """)
    
    if st.button("Face Dilemma 4.1 (+5 XP) ➔", use_container_width=True):
        if "d1_theory" not in st.session_state.completed_steps:
            st.session_state.xp += 5
            st.session_state.completed_steps.add("d1_theory")
        st.session_state.step = "dilemma_1"
        st.rerun()

elif st.session_state.step == "dilemma_1":
    st.caption("Dilemma 1 of 4 | Behavioral Diagnosis")
    st.subheader("Scenario: The Sinking Stock")
    st.write("**Dilemma:** You bought shares in Company Alpha at €50. The price drops sharply to €35 (-30%) due to structural insolvency. Independent analysts recommend moving capital into a diversified index fund. What do you do?")
    
    options = [
        ("Sell at €35, accept the loss, and move your money into a safer diversified fund.", 0, None),
        ("Hold onto the shares for a little bit longer with a strict limit to see if things improve.", 1, None),
        ("Refuse to sell until the price climbs back to €50, just so you don't officially admit a loss.", 2, "Preserver")
    ]
    
    if "d1_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d1_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d1_opts], index=None)
    
    if st.button("Confirm Choice (+10 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d1_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            if "dilemma_1" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("dilemma_1")
            del st.session_state.d1_opts
            st.session_state.step = "dilemma_2_theory"
            st.rerun()

# --- Module 4.2: Herd Mentality / FOMO ---
elif st.session_state.step == "dilemma_2_theory":
    st.caption("Level 4: Behavioral Diagnosis | Module 4.2 Awareness")
    st.subheader("Module 4.2: Herd Mentality & FOMO")
    st.info("🎯 **Behavioral Insight:** Understand the dangerous urge to follow crowds and social media hype without independent analysis.")
    
    st.markdown("""
    * **Herd Mentality:** Humans naturally feel safer copying the crowd. When everyone around you or on social media is buying an asset, your brain tricks you into thinking it must be a guaranteed win.
    * **FOMO (Fear Of Missing Out):** Watching others boast about quick profits triggers panic that you are being left behind. This emotional pressure leads people to buy at peak prices right before a crash.
    """)
    
    if st.button("Face Dilemma 4.2 (+5 XP) ➔", use_container_width=True):
        if "d2_theory" not in st.session_state.completed_steps:
            st.session_state.xp += 5
            st.session_state.completed_steps.add("d2_theory")
        st.session_state.step = "dilemma_2"
        st.rerun()

elif st.session_state.step == "dilemma_2":
    st.caption("Dilemma 2 of 4 | Behavioral Diagnosis")
    st.subheader("Scenario: The Viral Trend")
    st.write("**Dilemma:** A speculative crypto asset surges 400% in two weeks. Social media influencers boast quick wealth and urge buying. You have not analyzed its fundamentals. What do you do?")
    
    options = [
        ("Recognize the hype bubble, ignore the buzz, and stick to your long-term plan.", 0, None),
        ("Put in only a tiny amount of pocket money that you wouldn't mind losing completely.", 1, None),
        ("Jump in and invest a big chunk of your savings right away so you don't miss out on the gains.", 2, "Follower")
    ]
    
    if "d2_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d2_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d2_opts], index=None)
    
    if st.button("Confirm Choice (+10 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d2_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            if "dilemma_2" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("dilemma_2")
            del st.session_state.d2_opts
            st.session_state.step = "dilemma_3_theory"
            st.rerun()

# --- Module 4.3: Overconfidence & Illusion of Control ---
elif st.session_state.step == "dilemma_3_theory":
    st.caption("Level 4: Behavioral Diagnosis | Module 4.3 Awareness")
    st.subheader("Module 4.3: Overconfidence & Illusion of Control")
    st.info("🎯 **Behavioral Insight:** Beware of confusing luck with skill after short-term financial wins.")
    
    st.markdown("""
    * **Overconfidence Bias:** When people experience quick early success in markets, they tend to overestimate their own predictive abilities and underestimate true market risk.
    * **Illusion of Control:** Believing that your personal intuition or "gut feeling" can outsmart the market. This often leads to excessive trading, skipping homework, and taking dangerous financial bets.
    """)
    
    if st.button("Face Dilemma 4.3 (+5 XP) ➔", use_container_width=True):
        if "d3_theory" not in st.session_state.completed_steps:
            st.session_state.xp += 5
            st.session_state.completed_steps.add("d3_theory")
        st.session_state.step = "dilemma_3"
        st.rerun()

elif st.session_state.step == "dilemma_3":
    st.caption("Dilemma 3 of 4 | Behavioral Diagnosis")
    st.subheader("Scenario: The Winning Streak")
    st.write("**Dilemma:** After two consecutive winning stock trades during a market rally, you feel you possess superior market timing abilities. What is your next move?")
    
    options = [
        ("Realize that general market luck played a big role, keeping your core money safely diversified.", 0, None),
        ("Pause and do careful research on companies before risking any extra money.", 1, None),
        ("Move most of your savings into risky fast-trading because you feel your gut instincts can't fail.", 2, "Accumulator")
    ]
    
    if "d3_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d3_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d3_opts], index=None)
    
    if st.button("Confirm Choice (+10 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d3_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            if "dilemma_3" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("dilemma_3")
            del st.session_state.d3_opts
            st.session_state.step = "dilemma_4_theory"
            st.rerun()

# --- Module 4.4: Present Bias & Immediate Gratification ---
elif st.session_state.step == "dilemma_4_theory":
    st.caption("Level 4: Behavioral Diagnosis | Module 4.4 Awareness")
    st.subheader("Module 4.4: Present Bias & Immediate Gratification")
    st.info("🎯 **Behavioral Insight:** Notice how immediate desires constantly sabotage long-term financial freedom.")
    
    st.markdown("""
    * **Present Bias:** The powerful psychological tendency to value immediate rewards today far more than significantly larger rewards in the future.
    * **Immediate Gratification:** Spending money instantly on temporary pleasures (like trendy gadgets or clothes) delivers a quick dopamine hit, but repeatedly leaves you without savings or protection when real emergencies hit.
    """)
    
    if st.button("Face Dilemma 4.4 (+5 XP) ➔", use_container_width=True):
        if "d4_theory" not in st.session_state.completed_steps:
            st.session_state.xp += 5
            st.session_state.completed_steps.add("d4_theory")
        st.session_state.step = "dilemma_4"
        st.rerun()

elif st.session_state.step == "dilemma_4":
    st.caption("Dilemma 4 of 4 | Behavioral Diagnosis")
    st.subheader("Scenario: The Sudden Bonus")
    st.write("**Dilemma:** You receive an unexpected bonus of €1,000. You currently possess no emergency reserve. How do you allocate the funds?")
    
    options = [
        ("Put most of it (€700–€800) into an emergency fund to build an essential safety net.", 0, None),
        ("Split the money 50/50: half straight to savings and half for fun and shopping.", 1, None),
        ("Spend all €1,000 right now on shopping and fun items, leaving saving for sometime later in life.", 2, "Self-Control Deficiency")
    ]
    
    if "d4_opts" not in st.session_state:
        random.shuffle(options)
        st.session_state.d4_opts = options
        
    choice = st.radio("Choose your reaction:", [opt[0] for opt in st.session_state.d4_opts], index=None)
    
    if st.button("Complete Diagnostic Evaluation (+10 XP)", use_container_width=True):
        if choice is not None:
            selected = next(opt for opt in st.session_state.d4_opts if opt[0] == choice)
            st.session_state.bias_score += selected[1]
            if selected[2]:
                st.session_state.bias_flags.append(selected[2])
            if "dilemma_4" not in st.session_state.completed_steps:
                st.session_state.xp += 10
                st.session_state.completed_steps.add("dilemma_4")
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
        
    # Υπολογισμός χρόνου σε λεπτά με 1 δεκαδικό
    if "start_time" in st.session_state and st.session_state.start_time:
        elapsed_time = round((time.time() - st.session_state.start_time) / 60.0, 1)
    else:
        elapsed_time = 0.0

    save_result(st.session_state.user_name, st.session_state.xp, elapsed_time, score, archetype)
    
    st.subheader(f"Dominant Archetype: **{archetype}**")
    st.info(f"**Behavioral Profile:** {desc}")
    
    # Εμφάνιση metrics (Vulnerability + Χρόνος)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(label="Vulnerability Score (0–8 pts)", value=f"{score} / 8")
    with col_m2:
        st.metric(label="Completion Time", value=f"{elapsed_time} min")
    
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
