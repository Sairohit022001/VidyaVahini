from firestore.firestore_utils import (
    create_user_profile, get_user_profile, update_user_profile,
    delete_user_profile, user_exists, get_users_by_role, update_user_settings
)


def run_tests():
    user_id = "user_123"
    
    # Create user profile
    create_user_profile(user_id, {"name": "Rohi", "email": "rohi@example.com", "role": "student"})
    
    # Fetch and print user profile
    profile = get_user_profile(user_id)
    print("User profile after creation:", profile)
    
    # Update user profile role
    update_user_profile(user_id, {"role": "teacher"})
    
    # Check if user exists
    exists = user_exists(user_id)
    print(f"Does user exist? {exists}")
    
    # Get users by role 'teacher'
    users = get_users_by_role("teacher")
    print(f"Users with role 'teacher': {users}")
    
    # Update user settings
    update_user_settings(user_id, {"notifications": True, "theme": "dark"})
    
    # Fetch and print user profile after settings update
    profile = get_user_profile(user_id)
    print("User profile after settings update:", profile)
    
    # Delete user profile
    delete_user_profile(user_id)
    print(f"Deleted user profile for user_id: {user_id}")

if __name__ == "__main__":
    run_tests()
