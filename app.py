import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random

# =====================================================
# PHASE 1 PROMPT EFFICIENCY GAME
# Version: 1000 Random Challenge Bank
# =====================================================

LEADERBOARD_FILE = "leaderboard.csv"
CHALLENGE_BANK_FILE = "challenge_bank_1000.csv"


# =====================================================
# 1. BASIC TOKEN COUNTER
# =====================================================
def count_tokens(text):
    """
    Simple prototype token counter.
    For Phase 1 demo, word count is enough.
    Later, this can be replaced with a real tokenizer such as tiktoken.
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


# =====================================================
# 2. CHALLENGE BANK GENERATOR
# =====================================================
def generate_challenge_bank(total_questions=1000, seed=42):
    """
    Generates 1000 prompt compression game questions.
    Each challenge includes:
    - original_prompt
    - expected_meaning
    - meaning_groups used by the auto evaluator
    - category
    - difficulty
    """
    random.seed(seed)

    scenarios = [
        {
            "category": "Customer Service",
            "difficulty": "Easy",
            "situation": "a customer received a damaged product and wants a refund",
            "action": "write a polite customer service reply",
            "tone": "polite and professional",
            "requirements": [
                "apologize to the customer",
                "mention the damaged product issue",
                "ask for photos or evidence",
                "ask for the order number",
                "explain that the company will investigate or process the refund request"
            ],
            "meaning_groups": {
                "apology": ["sorry", "apologize", "apology", "maaf"],
                "damaged product": ["damaged", "broken", "defective", "faulty", "rosak"],
                "refund or return": ["refund", "return", "replacement", "credit"],
                "photos or evidence": ["photo", "photos", "picture", "image", "gambar", "evidence"],
                "order number": ["order number", "order no", "order id", "invoice", "order"],
                "investigation": ["investigate", "check", "review", "verify", "process"]
            }
        },
        {
            "category": "Logistics",
            "difficulty": "Easy",
            "situation": "a shipment is ready for pickup but the transporter has not arrived",
            "action": "write a short follow-up message to the logistics provider",
            "tone": "clear and firm",
            "requirements": [
                "mention that the shipment is ready for pickup",
                "ask for pickup status",
                "request estimated pickup time",
                "mention urgency or SLA",
                "ask them to confirm"
            ],
            "meaning_groups": {
                "ready pickup": ["ready", "pickup", "pick up", "collection"],
                "status": ["status", "update", "progress"],
                "estimated time": ["eta", "estimated", "time", "when"],
                "urgency": ["urgent", "sla", "priority", "delay"],
                "confirmation": ["confirm", "confirmation", "reply"]
            }
        },
        {
            "category": "Supplier Management",
            "difficulty": "Medium",
            "situation": "a supplier delivered non-conforming material that failed incoming inspection",
            "action": "write a message requesting corrective action",
            "tone": "professional and direct",
            "requirements": [
                "mention non-conforming material",
                "refer to incoming inspection failure",
                "request root cause analysis",
                "request corrective action",
                "ask for replacement or disposition plan"
            ],
            "meaning_groups": {
                "nonconforming": ["non-conforming", "nonconforming", "defect", "failed", "reject"],
                "incoming inspection": ["incoming", "iqc", "inspection", "receiving"],
                "root cause": ["root cause", "rca", "cause"],
                "corrective action": ["corrective", "correction", "action", "capa"],
                "replacement disposition": ["replacement", "replace", "disposition", "rework", "return"]
            }
        },
        {
            "category": "HR",
            "difficulty": "Easy",
            "situation": "a candidate has been shortlisted for an interview",
            "action": "write an interview invitation email",
            "tone": "friendly and professional",
            "requirements": [
                "congratulate or inform the candidate",
                "mention interview invitation",
                "provide date and time",
                "provide interview mode or location",
                "ask the candidate to confirm availability"
            ],
            "meaning_groups": {
                "candidate": ["candidate", "applicant", "shortlisted"],
                "interview": ["interview", "meeting", "discussion"],
                "date time": ["date", "time", "schedule", "slot"],
                "mode location": ["online", "onsite", "location", "teams", "zoom", "office"],
                "confirm availability": ["confirm", "availability", "available"]
            }
        },
        {
            "category": "Manufacturing",
            "difficulty": "Medium",
            "situation": "production output is below the daily target due to a bottleneck at testing",
            "action": "write a short production update to management",
            "tone": "clear and factual",
            "requirements": [
                "mention output is below target",
                "identify testing as the bottleneck",
                "state impact on delivery or production plan",
                "propose recovery action",
                "request support or decision if needed"
            ],
            "meaning_groups": {
                "below target": ["below", "short", "miss", "target", "output"],
                "testing bottleneck": ["test", "testing", "bottleneck", "capacity"],
                "impact": ["impact", "delay", "delivery", "plan", "schedule"],
                "recovery": ["recover", "recovery", "overtime", "second shift", "action"],
                "support decision": ["support", "decision", "approval", "help"]
            }
        },
        {
            "category": "Finance",
            "difficulty": "Medium",
            "situation": "a purchase order is still open and goods have not been received",
            "action": "write a short ERP follow-up note",
            "tone": "concise and business-like",
            "requirements": [
                "mention open purchase order",
                "mention goods not received",
                "ask for supplier delivery status",
                "check financial exposure or commitment",
                "request update in ERP"
            ],
            "meaning_groups": {
                "open po": ["open po", "purchase order", "po", "order"],
                "not received": ["not received", "pending receipt", "goods", "grn"],
                "delivery status": ["delivery", "status", "supplier", "eta"],
                "financial exposure": ["financial", "exposure", "commitment", "liability", "cash"],
                "erp update": ["erp", "update", "system", "record"]
            }
        },
        {
            "category": "Legal / Compliance",
            "difficulty": "Hard",
            "situation": "a design partner needs to carry a network card overseas for compatibility testing",
            "action": "write a request to legal for an undertaking or disclaimer",
            "tone": "formal and risk-aware",
            "requirements": [
                "mention the network card purpose",
                "state it is for compatibility or topology testing",
                "mention export control check",
                "require return in good condition",
                "include risk protection or undertaking"
            ],
            "meaning_groups": {
                "network card": ["network card", "nic", "card"],
                "testing purpose": ["compatibility", "topology", "testing", "optimization"],
                "export control": ["export", "control", "cross border", "customs"],
                "return condition": ["return", "returned", "good condition"],
                "undertaking risk": ["undertaking", "disclaimer", "risk", "liability", "legal"]
            }
        },
        {
            "category": "Sales",
            "difficulty": "Easy",
            "situation": "a customer asks for a revised quotation with better pricing",
            "action": "write a sales reply asking for volume and target price",
            "tone": "positive and professional",
            "requirements": [
                "acknowledge the quotation request",
                "ask for expected order volume",
                "ask for target price",
                "mention internal review",
                "promise to revert with updated quotation"
            ],
            "meaning_groups": {
                "quotation": ["quotation", "quote", "pricing", "price"],
                "volume": ["volume", "quantity", "qty", "forecast"],
                "target price": ["target price", "target", "budget"],
                "internal review": ["review", "internal", "management", "team"],
                "revert": ["revert", "reply", "update", "send"]
            }
        },
        {
            "category": "Quality",
            "difficulty": "Medium",
            "situation": "a customer reported a field failure after product shipment",
            "action": "write an initial quality response",
            "tone": "serious and customer-focused",
            "requirements": [
                "acknowledge the field failure",
                "apologize for the issue",
                "ask for failure details and evidence",
                "request affected quantity or serial numbers",
                "commit to investigation and containment"
            ],
            "meaning_groups": {
                "field failure": ["field failure", "failure", "fail", "issue"],
                "apology": ["sorry", "apologize", "apology"],
                "details evidence": ["details", "evidence", "photo", "log", "report"],
                "quantity serial": ["quantity", "serial", "sn", "affected"],
                "investigation containment": ["investigate", "containment", "check", "analysis"]
            }
        },
        {
            "category": "AI Prompting",
            "difficulty": "Hard",
            "situation": "a user writes a long local dialect message and wants it converted into a short standard AI prompt",
            "action": "write an instruction for converting dialect input into token-efficient standard language",
            "tone": "clear and technical",
            "requirements": [
                "preserve the original intent",
                "convert dialect or mixed language into standard language",
                "reduce unnecessary words",
                "keep important entities and constraints",
                "produce a short AI-ready prompt"
            ],
            "meaning_groups": {
                "preserve intent": ["intent", "meaning", "preserve", "retain"],
                "dialect standard": ["dialect", "mixed", "standard", "language"],
                "reduce words": ["short", "concise", "reduce", "compress"],
                "entities constraints": ["entities", "constraint", "requirements", "important"],
                "ai prompt": ["ai", "prompt", "ready", "instruction"]
            }
        }
    ]

    modifiers = [
        "for a Malaysian SME context",
        "for a regional operations team",
        "for a senior manager audience",
        "for a new startup team",
        "for a manufacturing company",
        "for an e-commerce business",
        "for a logistics coordinator",
        "for an internal management update",
        "for a customer-facing response",
        "for a supplier-facing message"
    ]

    extra_constraints = [
        "Keep it under 80 words.",
        "Use simple business English.",
        "Avoid legal jargon unless needed.",
        "Make the message polite but firm.",
        "Use a concise email style.",
        "Make it suitable for WhatsApp or Teams.",
        "Do not overpromise.",
        "Mention next action clearly.",
        "Keep the tone calm and practical.",
        "Make it understandable to non-technical users."
    ]

    challenge_rows = []

    for i in range(1, total_questions + 1):
        scenario = random.choice(scenarios)
        modifier = random.choice(modifiers)
        constraint = random.choice(extra_constraints)

        requirements_text = " ".join(
            [f"It should {req}." for req in scenario["requirements"]]
        )

        original_prompt = (
            f"Please {scenario['action']} about {scenario['situation']} {modifier}. "
            f"The tone should be {scenario['tone']}. {requirements_text} {constraint}"
        )

        expected_meaning = "The compressed prompt should still include: " + "; ".join(scenario["requirements"])

        challenge_id = f"Q{i:04d}"

        challenge_rows.append({
            "challenge_id": challenge_id,
            "category": scenario["category"],
            "difficulty": scenario["difficulty"],
            "original_prompt": original_prompt,
            "expected_meaning": expected_meaning,
            "meaning_groups": scenario["meaning_groups"]
        })

    return challenge_rows


# =====================================================
# 3. AUTOMATIC MEANING CHECKER
# =====================================================
def auto_meaning_score(player_prompt, meaning_groups):
    """
    Rule-based checker.
    It checks whether the compressed prompt still contains the key meanings.
    """
    text = player_prompt.lower().strip()

    if not text:
        return 0, "Empty reply"

    words = text.split()

    if len(words) < 5:
        return 0, "Too short to carry the required meaning"

    unique_words = set(words)
    unique_ratio = len(unique_words) / len(words)

    if unique_ratio < 0.4:
        return 0, "Likely repeated or nonsense words"

    vowels = sum(1 for c in text if c in "aeiou")
    letters = sum(1 for c in text if c.isalpha())
    if letters > 10 and vowels / max(letters, 1) < 0.15:
        return 0, "Likely gibberish or unreadable text"

    matched_groups = 0
    missing_groups = []

    for group_name, keywords in meaning_groups.items():
        if any(keyword.lower() in text for keyword in keywords):
            matched_groups += 1
        else:
            missing_groups.append(group_name)

    accuracy_score = round((matched_groups / len(meaning_groups)) * 100)

    if accuracy_score < 70:
        reason = "Missing key meaning: " + ", ".join(missing_groups)
    else:
        reason = "Meaning is sufficiently preserved"

    return accuracy_score, reason


# =====================================================
# 4. SCORE CALCULATION
# =====================================================
def calculate_token_saving(original_tokens, player_tokens):
    if original_tokens == 0:
        return 0

    saving = ((original_tokens - player_tokens) / original_tokens) * 100
    return max(0, saving)


def calculate_final_score(accuracy_score, token_saving_percent):
    if accuracy_score < 70:
        return 0

    return accuracy_score * (token_saving_percent / 100)


def get_badge(final_score):
    if final_score >= 70:
        return "🏆 Master Compressor"
    elif final_score >= 50:
        return "🥇 Efficient Prompter"
    elif final_score >= 30:
        return "🥈 Good Attempt"
    elif final_score > 0:
        return "🥉 Needs Improvement"
    else:
        return "❌ No Score"


# =====================================================
# 5. EXPORT CHALLENGE BANK
# =====================================================
def save_challenge_bank_to_csv(challenges):
    export_rows = []
    for c in challenges:
        export_rows.append({
            "challenge_id": c["challenge_id"],
            "category": c["category"],
            "difficulty": c["difficulty"],
            "original_prompt": c["original_prompt"],
            "expected_meaning": c["expected_meaning"]
        })
    df = pd.DataFrame(export_rows)
    df.to_csv(CHALLENGE_BANK_FILE, index=False)
    return df


# =====================================================
# 6. STREAMLIT PAGE SETUP
# =====================================================
st.set_page_config(
    page_title="Prompt Efficiency Challenge",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Prompt Efficiency Challenge")
st.write(
    "Phase 1 game prototype with 1000 random challenge questions. "
    "Players compress long prompts while preserving meaning."
)


# =====================================================
# 7. LOAD OR GENERATE CHALLENGES
# =====================================================
if "challenges" not in st.session_state:
    st.session_state.challenges = generate_challenge_bank(total_questions=1000, seed=42)

if "current_challenge" not in st.session_state:
    st.session_state.current_challenge = random.choice(st.session_state.challenges)


# =====================================================
# 8. SIDEBAR CONTROLS
# =====================================================
st.sidebar.header("Game Controls")

player_name = st.sidebar.text_input(
    "Player Name",
    placeholder="Enter your name or nickname"
)

categories = sorted(list(set(c["category"] for c in st.session_state.challenges)))
difficulties = sorted(list(set(c["difficulty"] for c in st.session_state.challenges)))

selected_category = st.sidebar.selectbox("Category", ["Random"] + categories)
selected_difficulty = st.sidebar.selectbox("Difficulty", ["Random"] + difficulties)

if st.sidebar.button("Generate Random Question"):
    filtered = st.session_state.challenges

    if selected_category != "Random":
        filtered = [c for c in filtered if c["category"] == selected_category]

    if selected_difficulty != "Random":
        filtered = [c for c in filtered if c["difficulty"] == selected_difficulty]

    if filtered:
        st.session_state.current_challenge = random.choice(filtered)
    else:
        st.sidebar.warning("No question found for this filter.")

challenge_ids = [c["challenge_id"] for c in st.session_state.challenges]
selected_challenge_id = st.sidebar.selectbox("Or select Challenge ID", challenge_ids)

if st.sidebar.button("Load Selected Challenge"):
    selected = [c for c in st.session_state.challenges if c["challenge_id"] == selected_challenge_id]
    if selected:
        st.session_state.current_challenge = selected[0]

st.sidebar.divider()

challenge_bank_df = save_challenge_bank_to_csv(st.session_state.challenges)
st.sidebar.download_button(
    label="Download 1000 Question Bank CSV",
    data=challenge_bank_df.to_csv(index=False).encode("utf-8"),
    file_name="challenge_bank_1000.csv",
    mime="text/csv"
)


# =====================================================
# 9. CURRENT CHALLENGE DISPLAY
# =====================================================
challenge = st.session_state.current_challenge
original_prompt = challenge["original_prompt"]
original_tokens = count_tokens(original_prompt)

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader(f"Challenge {challenge['challenge_id']}")
    st.info(original_prompt)

with right_col:
    st.subheader("Question Info")
    st.write(f"**Category:** {challenge['category']}")
    st.write(f"**Difficulty:** {challenge['difficulty']}")
    st.write(f"**Original Token Count:** {original_tokens}")

    with st.expander("Expected Meaning"):
        st.write(challenge["expected_meaning"])


# =====================================================
# 10. PLAYER INPUT
# =====================================================
st.subheader("Your Compressed Prompt")

player_prompt = st.text_area(
    "Rewrite the prompt using fewer words while keeping the same meaning:",
    height=160,
    placeholder="Type your compressed prompt here..."
)


# =====================================================
# 11. SCORE CALCULATION
# =====================================================
if st.button("Calculate Score", type="primary"):
    if not player_prompt.strip():
        st.warning("Please enter your compressed prompt first.")
    else:
        player_tokens = count_tokens(player_prompt)
        token_saving = calculate_token_saving(original_tokens, player_tokens)
        accuracy_score, evaluation_reason = auto_meaning_score(
            player_prompt,
            challenge["meaning_groups"]
        )
        final_score = calculate_final_score(accuracy_score, token_saving)
        badge = get_badge(final_score)

        st.subheader("Result")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Original Tokens", original_tokens)

        with col2:
            st.metric("Your Tokens", player_tokens)

        with col3:
            st.metric("Token Saving", f"{token_saving:.2f}%")

        with col4:
            st.metric("Meaning Accuracy", f"{accuracy_score}%")

        with col5:
            st.metric("Final Score", f"{final_score:.2f}")

        st.write(f"**Badge:** {badge}")
        st.write(f"**Evaluation Reason:** {evaluation_reason}")

        if player_tokens >= original_tokens:
            st.warning(
                "Your prompt is not shorter than the original prompt. "
                "Token saving is counted as 0%."
            )

        if accuracy_score < 70:
            st.error(
                "Meaning accuracy is below 70%, so the final score is 0. "
                "The compressed prompt lost too much meaning or looks like nonsense."
            )
        else:
            st.success(
                "Good attempt. The prompt is shorter and the main meaning is still preserved."
            )

        result = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player_name": player_name if player_name.strip() else "Anonymous",
            "challenge_id": challenge["challenge_id"],
            "category": challenge["category"],
            "difficulty": challenge["difficulty"],
            "original_tokens": original_tokens,
            "player_tokens": player_tokens,
            "token_saving_percent": round(token_saving, 2),
            "accuracy_score": accuracy_score,
            "final_score": round(final_score, 2),
            "badge": badge,
            "evaluation_reason": evaluation_reason,
            "original_prompt": original_prompt,
            "player_prompt": player_prompt
        }

        if os.path.exists(LEADERBOARD_FILE):
            leaderboard = pd.read_csv(LEADERBOARD_FILE)
            leaderboard = pd.concat(
                [leaderboard, pd.DataFrame([result])],
                ignore_index=True
            )
        else:
            leaderboard = pd.DataFrame([result])

        leaderboard.to_csv(LEADERBOARD_FILE, index=False)
        st.info("Result saved to leaderboard.")


# =====================================================
# 12. LEADERBOARD DISPLAY
# =====================================================
st.subheader("Leaderboard")

if os.path.exists(LEADERBOARD_FILE):
    leaderboard = pd.read_csv(LEADERBOARD_FILE)
    leaderboard = leaderboard.sort_values(by="final_score", ascending=False)

    display_columns = [
        "datetime",
        "player_name",
        "challenge_id",
        "category",
        "difficulty",
        "original_tokens",
        "player_tokens",
        "token_saving_percent",
        "accuracy_score",
        "final_score",
        "badge"
    ]

    st.dataframe(
        leaderboard[display_columns],
        use_container_width=True
    )

    with st.expander("View submitted prompts and evaluation reasons"):
        st.dataframe(
            leaderboard[
                [
                    "player_name",
                    "challenge_id",
                    "original_prompt",
                    "player_prompt",
                    "evaluation_reason",
                    "final_score"
                ]
            ],
            use_container_width=True
        )

    st.download_button(
        label="Download Leaderboard CSV",
        data=leaderboard.to_csv(index=False).encode("utf-8"),
        file_name="leaderboard.csv",
        mime="text/csv"
    )
else:
    st.write("No results yet.")


# =====================================================
# 13. PROTOTYPE NOTE
# =====================================================
st.caption(
    "Prototype note: This version creates 1000 random text-based challenges using templates. "
    "The meaning checker is rule-based. In the next version, it can be upgraded with an AI evaluator model."
)
