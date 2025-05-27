from firebase_utils import save_plan, load_plan

test_user_id = "testuser123"
test_plan = {
    "destination": "Paris",
    "plan": "See Eiffel Tower and eat croissants!"
}

save_plan(test_user_id, test_plan)
result = load_plan(test_user_id)
print("Loaded plan from Firebase:", result)
