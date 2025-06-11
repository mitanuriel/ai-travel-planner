import streamlit as st
from file_utils import extract_text_from_pdf, extract_text_from_txt
from firebase_utils import save_plan, load_plan
from gemini_utils import call_gemini_api


st.set_page_config(page_title="Travel Wizard", layout="wide")

st.markdown("""
<div style='text-align: center;'>
    <h1>Travel Wizard</h1>
    <h6>Plan your trip with the help of AI! Upload your travel documents, pick a destination and interests, and let our app create your itinerary.</h6>
</div>
""", unsafe_allow_html=True)

with open("src/custom_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


USER_ID = "Elina"

#Layout 
left_col, right_col = st.columns(2)

# --- Left column and main user form ---
with left_col:
    st.header("Create or Update Your Travel Plan")

    with st.form("plan_form"):
        destination = st.text_input("Destination", placeholder="e.g. Paris")
        dates = st.date_input("Travel Dates", [])
        interests = st.multiselect(
            "Select your interests:",
            ["Nature", "Food & Dining", "Museums", "Shopping", "Nightlife", 
             "Hiking", "History", "Relaxation", "Family", "Local Culture"]
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
            st.subheader("Extracted text from files")
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
                st.success("Plan saved!")
            else:
                st.warning("Please fill in destination and plan.")

# --- Right Column: Generated plan and display section ---
with right_col:

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
        st.info("No plan found yet. Fill in the form and save your plan.")

        # --- Gemini AI integration ---
    if st.button("Generate plan with a Travel Wizard", key="generate_plan_button"):
        prompt = (
            f"You are an expert travel planner. "
            f"Create a detailed, day-by-day itinerary for a trip to {destination} "
            f"on these dates: {dates}.\n"
            f"User's interests: {', '.join(interests)}.\n"
            f"End your response with a Markdown table listing each day, morning, afternoon, and evening activities, plus any notes."
        )
        if extracted_texts:
            prompt += "Here are some documents or notes to consider:\n"
            for text in extracted_texts:
                prompt += text[:1000] + "\n"
        prompt += f"User's own notes: {plan}"

        st.info("Contacting travel planner …")
        response = call_gemini_api(prompt)
        st.success("Travel Wizard-Generated Travel Plan:")
        st.markdown(
            f'<div class="ai-plan-box">{response}</div>',
            unsafe_allow_html=True
        )


    st.markdown('</div>', unsafe_allow_html=True)