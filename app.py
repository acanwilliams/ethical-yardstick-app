
import streamlit as st
import json
from datetime import datetime
import uuid
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Ethical Yardstick", layout="centered")

# Display the branded yardstick image at the top
st.image("ethical_yardstick_preview.png", use_container_width=True)

st.title("🧭 Ethical Yardstick")
st.subheader("by April C. Williams — The Ethical Data Doc")

DATA_FILE = "ethical_yardstick_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"entries": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def interpret_score(avg_score):
    if avg_score >= 4.5:
        return "✅ Extremely Ethical"
    elif avg_score >= 3.5:
        return "👍 Mostly Ethical"
    elif avg_score >= 2.0:
        return "⚠️ Ethically Concerning"
    else:
        return "❌ Not Ethical at All"

criteria = [
    "Justice & Equity",
    "Transparency & Trust",
    "Accountability",
    "Respect for Persons",
    "Non-Maleficence"
]

st.markdown("Use this ethical yardstick to evaluate a use case through a Do No Harm lens.")

use_case = st.text_area("Describe the Use Case")
response = st.text_area("Describe the Response")

scores = {}
justifications = {}

if use_case and response:
    st.markdown("### Rubric Evaluation")
    for criterion in criteria:
        scores[criterion] = st.slider(f"{criterion} (0-5)", 0, 5, 3)
        justifications[criterion] = st.text_area(f"Why did you score '{criterion}' this way?", key=criterion)

    if st.button("Submit Evaluation"):
        entry = {
            "entry_id": str(uuid.uuid4()),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "use_case": use_case,
            "response": response,
            "scores": scores,
            "justifications": justifications
        }
        data = load_data()
        data["entries"].append(entry)
        save_data(data)
        st.success("✅ Evaluation saved successfully!")

st.markdown("### 📚 Most Recent Evaluation")

data = load_data()
if data["entries"]:
    latest = data["entries"][-1]
    st.markdown(f"**Use Case:** {latest['use_case']}")
    st.markdown(f"**Response:** {latest['response']}")

    avg_score = sum(latest["scores"].values()) / len(criteria)
    result = interpret_score(avg_score)
    st.markdown(f"**Overall Score:** {avg_score:.2f} — {result}")

    # Display yardstick image again for visual representation
    st.image("ethical_yardstick_preview.png", use_container_width=True)
else:
    st.info("No evaluations submitted yet.")
