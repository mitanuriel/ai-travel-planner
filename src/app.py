import streamlit as st

st.set_page_config(page_title="AI Travel Planner", page_icon="🧳")

# --- Sidebar or header ---
st.title("AI Travel Planner 🧳")
st.write(
    "Plan your trip with the help of AI! "
    "Upload your travel documents, pick a destination and interests, "
    "and let our app create your itinerary."
)

# --- Destination and Dates ---
destination = st.text_input("Destination")
dates = st.date_input("Travel Dates", [])

# --- Interests ---
interests = st.multiselect(
    "Select your interests:",
    ["Nature", "Food & Dining", "Museums", "Shopping", "Nightlife", "Hiking", "History", "Relaxation", "Family", "Local Culture"]
)

# --- File Upload ---
uploaded_files = st.file_uploader(
    "Upload your travel documents (PDF or TXT)", 
    type=["pdf", "txt"], 
    accept_multiple_files=True
)

# --- Button ---
if st.button("Generate Plan"):
    st.info("🔄 This is where the AI-generated travel plan will appear (not yet implemented).")

# --- Placeholder for result ---
st.markdown("---")
st.subheader("Your Personalized Travel Plan")
st.write("Your plan will show up here after you click 'Generate Plan'.")

