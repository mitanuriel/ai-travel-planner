import streamlit as st
from file_utils import extract_text_from_pdf, extract_text_from_txt

st.set_page_config(page_title="AI Travel Planner", page_icon="🧳")

st.title("AI Travel Planner 🧳")
st.write(
    "Plan your trip with the help of AI! "
    "Upload your travel documents, pick a destination and interests, "
    "and let our app create your itinerary."
)

destination = st.text_input("Destination")
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
        # Show only first 500 characters as preview
        st.text_area(f"Extracted from {file.name}", text[:500], height=100)

if st.button("Generate Plan"):
    st.info("🔄 This is where the AI-generated travel plan will appear (not yet implemented).")
    # Later, pass extracted_texts to Gemini API
