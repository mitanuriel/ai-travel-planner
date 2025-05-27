import streamlit as st
from file_utils import extract_text_from_pdf, extract_text_from_txt
from firebase_utils import save_plan, load_plan

st.set_page_config(page_title="AI Travel Planner", page_icon="🧳")

USER_ID = "user123"

st.title("AI Travel Planner 🧳")
st.write(
    "Plan your trip with the help of AI! "
    "Upload your travel documents, pick a destination and interests, "
    "and let our app create your itinerary."
)

st.header("Create or Update Your Travel Plan")

# --- Main user form ---
with st.form("plan_form"):
    destination = st.text_input("Destination", placeholder="e.g. Paris")
    dates = st.date_input("Travel Dates", [])
    interests = st.multiselect(
        "Select your interests:",
        ["Nature", "Food & Dining", "Museums", "Shopping", "Nightlife", "Hiking", "History", "Relaxation", "Family", "Local Culture"]
    )
    uploaded_files = st.file_uploader(
        "Upload your travel documents (PDF or TXT)", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    plan = st.text_area("Trip plan", placeholder="What do you want to do there?")

    submitted = st.form_submit_button("Save Plan")

    extracted_texts = []

    if uploaded_files:
        st.subheader("Extracted Text from Files")
        for file in uploaded_files:
            if file.name.endswith(".pdf"):
                text = extract_text_from_pdf(file)
            elif file.name.endswith(".txt"):
                text = extract_text_from_txt(file)
            else:
                text = ""
            extracted_texts.append(text)
            st.text_area(f"Extracted from {file.name}", text[:1000], height=200)

    if submitted:
        if destination and plan:
            plan_data = {
                "destination": destination,
                "dates": str(dates),
                "interests": interests,
                "plan": plan,
                "extracted_texts": extracted_texts,
            }
            save_plan(USER_ID, plan_data)
            st.success("Plan saved to Firebase!")
        else:
            st.warning("Please fill in destination and plan.")

# --- Display the latest saved plan ---
st.header("Your Latest Saved Plan")

saved_plan = load_plan(USER_ID)
if saved_plan:
    st.write(f"**Destination:** {saved_plan.get('destination')}")
    st.write(f"**Dates:** {saved_plan.get('dates')}")
    st.write(f"**Interests:** {', '.join(saved_plan.get('interests', []))}")
    st.write(f"**Plan:** {saved_plan.get('plan')}")
    if saved_plan.get('extracted_texts'):
        st.subheader("Previously Extracted Texts")
        for idx, txt in enumerate(saved_plan['extracted_texts']):
            st.text_area(f"Extracted text #{idx+1}", txt[:1000], height=200)
else:
    st.info("No plan found yet. Fill in the form above and save your plan.")

# --- Placeholder for Generate Plan button (future Gemini AI integration) ---
if st.button("Generate AI Plan"):
    st.info("🔄 This is where the AI-generated travel plan will appear (not yet implemented).")
