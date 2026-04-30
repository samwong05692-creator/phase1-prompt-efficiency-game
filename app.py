import streamlit as st
import pandas as pd
from datetime import datetime
import os


# =====================================================
# 1. BASIC TOKEN COUNTER
# =====================================================
def count_tokens(text):
    """
    Simple prototype token counter.
    For Phase 1 demo, word count is enough.
    Later, this can be replaced with a real AI tokenizer.
    """
    if not text.strip():
        return 0
    return len(text.split())


# =====================================================
# 2. AUTOMATIC MEANING CHECKER
# =====================================================
def auto_meaning_score(player_prompt):
    """
    Simple rule-based meaning checker for prototype.

    It checks whether the compressed prompt still contains
    the key meaning from the original prompt.
    """

    text = player_prompt.lower().strip()

    if not text:
        return 0, "Empty reply"

    words = text.split()

    # Too short to carry meaning
    if len(words) < 5:
        return 0, "Too short to carry the required meaning"

    # Repeated nonsense check
    unique_words = set(words)
    unique_ratio = len(unique_words) / len(words)

    if unique_ratio < 0.4:
        return 0, "Likely repeated or nonsense words"

    # Required meaning groups
    meaning_groups = {
        "apology": ["sorry", "apologize", "apology", "maaf"],
        "damaged product": ["damaged", "broken", "defective", "faulty", "rosak"],
        "refund or return": ["refund", "return", "replacement", "credit"],
        "photos or evidence": ["photo", "photos", "picture", "image", "gambar", "evidence"],
        "order number": ["order number", "order no", "order id", "invoice", "order"],
        "investigation or checking": ["investigate", "check", "review", "verify", "process"]
    }

    matched_groups = 0
    missing_groups = []

    for group_name, keywords in meaning_groups.items():
        if any(keyword in text for keyword in keywords):
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
# 3. TOKEN SAVING CALCULATION
# =====================================================
def calculate_token_saving(original_tokens, player_tokens):
    """
    Calculates token saving percentage.
    If player prompt is longer than original, saving becomes 0.
    """

    if original_tokens == 0:
        return 0

    saving = ((original_tokens - player_tokens) / original_tokens) * 100

    return max(0, saving)


# =====================================================
# 4. FINAL SCORE CALCULATION
# =====================================================
def calculate_final_score(accuracy_score, token_saving_percent):
    """
    Rule:
    If meaning accuracy is below 70%, final score becomes zero.
    This prevents nonsense short replies from winning.
    """

    if accuracy_score < 70:
        return 0

    return accuracy_score * (token_saving_percent / 100)


# =====================================================
# 5. DEFAULT CHALLENGE
# =====================================================
original_prompt = """
Please write a polite customer service reply to a customer who received a damaged product and wants a refund.
The reply should apologize, explain that the company will investigate, and ask the customer to provide photos and order number.
"""

expected_meaning = """
The compressed prompt should still ask the AI to:
1. Write a polite customer service reply.
2. Apologize to the customer.
3. Mention the damaged product issue.
4. Ask for photos or evidence.
5. Ask for order number.
6. Explain that the company will investigate, verify, or process the refund request.
"""


# =====================================================
# 6. STREAMLIT PAGE SETUP
# =====================================================
st.set_page_config(
    page_title="Prompt Efficiency Challenge",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 Prompt Efficiency Challenge")
st.write(
    "Rewrite the original prompt using fewer words while keeping the same meaning. "
    "The system will score both token saving and meaning accuracy."
)


# =====================================================
# 7. SHOW ORIGINAL PROMPT
# =====================================================
st.subheader("Original Prompt")
st.info(original_prompt)

original_tokens = count_tokens(original_prompt)

st.write(f"**Original Token Count:** {original_tokens}")


# =====================================================
# 8. SHOW EXPECTED MEANING
# =====================================================
with st.expander("View expected meaning"):
    st.write(expected_meaning)


# =====================================================
# 9. PLAYER INPUT
# =====================================================
st.subheader("Your Compressed Prompt")

player_name = st.text_input(
    "Player Name",
    placeholder="Enter your name or nickname"
)

player_prompt = st.text_area(
    "Type your shorter prompt here:",
    height=150,
    placeholder="Example: Write polite refund reply for damaged item. Apologize, ask photos/order number, say company will investigate."
)


# =====================================================
# 10. CALCULATE SCORE
# =====================================================
if st.button("Calculate Score"):
    if not player_prompt.strip():
        st.warning("Please enter your compressed prompt first.")

    else:
        player_tokens = count_tokens(player_prompt)
        token_saving = calculate_token_saving(original_tokens, player_tokens)

        accuracy_score, evaluation_reason = auto_meaning_score(player_prompt)

        final_score = calculate_final_score(
            accuracy_score,
            token_saving
        )

        st.subheader("Result")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Original Tokens", original_tokens)

        with col2:
            st.metric("Your Tokens", player_tokens)

        with col3:
            st.metric("Token Saving", f"{token_saving:.2f}%")

        with col4:
            st.metric("Final Score", f"{final_score:.2f}")

        st.write(f"**Meaning Accuracy:** {accuracy_score}%")
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

        # =====================================================
        # 11. SAVE RESULT TO LEADERBOARD
        # =====================================================
        result = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player_name": player_name if player_name.strip() else "Anonymous",
            "original_tokens": original_tokens,
            "player_tokens": player_tokens,
            "token_saving_percent": round(token_saving, 2),
            "accuracy_score": accuracy_score,
            "final_score": round(final_score, 2),
            "evaluation_reason": evaluation_reason,
            "player_prompt": player_prompt
        }

        leaderboard_file = "leaderboard.csv"

        if os.path.exists(leaderboard_file):
            leaderboard = pd.read_csv(leaderboard_file)
            leaderboard = pd.concat(
                [leaderboard, pd.DataFrame([result])],
                ignore_index=True
            )
        else:
            leaderboard = pd.DataFrame([result])

        leaderboard.to_csv(leaderboard_file, index=False)

        st.info("Result saved to leaderboard.")


# =====================================================
# 12. LEADERBOARD DISPLAY
# =====================================================
st.subheader("Leaderboard")

leaderboard_file = "leaderboard.csv"

if os.path.exists(leaderboard_file):
    leaderboard = pd.read_csv(leaderboard_file)

    leaderboard = leaderboard.sort_values(
        by="final_score",
        ascending=False
    )

    display_columns = [
        "datetime",
        "player_name",
        "original_tokens",
        "player_tokens",
        "token_saving_percent",
        "accuracy_score",
        "final_score"
    ]

    st.dataframe(
        leaderboard[display_columns],
        use_container_width=True
    )

    with st.expander("View submitted prompts"):
        st.dataframe(
            leaderboard[
                [
                    "player_name",
                    "player_prompt",
                    "evaluation_reason",
                    "final_score"
                ]
            ],
            use_container_width=True
        )

else:
    st.write("No results yet.")


# =====================================================
# 13. FOOTNOTE FOR PROTOTYPE
# =====================================================
st.caption(
    "Prototype note: This version uses simple rule-based meaning checking. "
    "In the next version, this can be upgraded with an AI evaluator model."
)
