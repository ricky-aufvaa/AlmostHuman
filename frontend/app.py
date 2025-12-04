import streamlit as st
import requests
import json
from typing import Optional

# Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def make_request(endpoint: str, method: str = "GET", data: dict = None, auth_required: bool = False) -> Optional[dict]:
    """Make API request with error handling"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if auth_required and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure the FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

def login_user(email: str, password: str) -> bool:
    """Login user and store token"""
    data = {"email": email, "password": password}
    response = make_request("/signin", "POST", data)
    
    if response:
        st.session_state.token = response["access_token"]
        st.session_state.authenticated = True
        
        # Get user profile
        profile = make_request("/profile", auth_required=True)
        if profile:
            st.session_state.user_info = profile
        
        return True
    return False

def signup_user(email: str, username: str, password: str) -> bool:
    """Sign up new user"""
    data = {"email": email, "username": username, "password": password}
    response = make_request("/signup", "POST", data)
    
    if response:
        st.session_state.token = response["access_token"]
        st.session_state.authenticated = True
        
        # Get user profile
        profile = make_request("/profile", auth_required=True)
        if profile:
            st.session_state.user_info = profile
        
        return True
    return False

def logout_user():
    """Logout user and clear session"""
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user_info = None
    st.session_state.chat_history = []

def forgot_password(email: str) -> Optional[str]:
    """Request password reset code"""
    data = {"email": email}
    response = make_request("/forgot-password", "POST", data)
    
    if response:
        return response.get("reset_code")  # For mock implementation
    return None

def reset_password(email: str, reset_code: str, new_password: str) -> bool:
    """Reset password with code"""
    data = {"email": email, "reset_code": reset_code, "new_password": new_password}
    response = make_request("/reset-password", "POST", data)
    
    return response is not None

def query_rag(question: str) -> Optional[str]:
    """Query the RAG system"""
    data = {"question": question, "session_id": "streamlit_session"}
    response = make_request("/query", "POST", data, auth_required=True)
    
    if response:
        return response["answer"]
    return None

def main():
    st.set_page_config(
        page_title="RAG System with Authentication",
        layout="wide"
    )
    
    st.title("RAG System with Authentication")
    
    # Check API health
    health = make_request("/health")
    if not health:
        st.error("API server is not responding. Please start the FastAPI server.")
        st.stop()
    
    # Authentication section
    if not st.session_state.authenticated:
        st.header("Authentication Required")
        
        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
        
        with tab1:
            st.subheader("Login to your account")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Login")
                
                if submit_login:
                    if email and password:
                        if login_user(email, password):
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Login failed. Please check your credentials.")
                    else:
                        st.error("Please fill in all fields.")
        
        with tab2:
            st.subheader("Create a new account")
            with st.form("signup_form"):
                email = st.text_input("Email", key="signup_email")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Sign Up")
                
                if submit_signup:
                    if email and username and password and confirm_password:
                        if password != confirm_password:
                            st.error("Passwords do not match.")
                        elif len(password) < 6:
                            st.error("Password must be at least 6 characters long.")
                        else:
                            if signup_user(email, username, password):
                                st.success("Account created successfully!")
                                st.rerun()
                            else:
                                st.error("Sign up failed. Email might already be registered.")
                    else:
                        st.error("Please fill in all fields.")
        
        with tab3:
            st.subheader("Reset your password")
            
            # Initialize session state for forgot password flow
            if "reset_step" not in st.session_state:
                st.session_state.reset_step = 1
            if "reset_email" not in st.session_state:
                st.session_state.reset_email = ""
            if "reset_code" not in st.session_state:
                st.session_state.reset_code = ""
            
            if st.session_state.reset_step == 1:
                # Step 1: Request reset code
                st.write("Enter your email address to receive a reset code:")
                with st.form("forgot_password_form"):
                    email = st.text_input("Email", key="forgot_email")
                    submit_forgot = st.form_submit_button("Send Reset Code")
                    
                    if submit_forgot:
                        if email:
                            reset_code = forgot_password(email)
                            if reset_code:
                                st.session_state.reset_email = email
                                st.session_state.reset_code = reset_code
                                st.session_state.reset_step = 2
                                st.success(f"Reset code sent! Your code is: **{reset_code}**")
                                st.info("In a real application, this code would be sent to your email.")
                                st.rerun()
                            else:
                                st.error("Failed to send reset code. Please check your email address.")
                        else:
                            st.error("Please enter your email address.")
            
            elif st.session_state.reset_step == 2:
                # Step 2: Enter reset code and new password
                st.write(f"Reset code has been sent to: **{st.session_state.reset_email}**")
                st.info(f"Your reset code is: **{st.session_state.reset_code}**")
                
                with st.form("reset_password_form"):
                    reset_code_input = st.text_input("Enter Reset Code")
                    new_password = st.text_input("New Password", type="password", key="reset_new_password")
                    confirm_new_password = st.text_input("Confirm New Password", type="password", key="reset_confirm_password")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit_reset = st.form_submit_button("Reset Password")
                    with col2:
                        cancel_reset = st.form_submit_button("Cancel")
                    
                    if cancel_reset:
                        st.session_state.reset_step = 1
                        st.session_state.reset_email = ""
                        st.session_state.reset_code = ""
                        st.rerun()
                    
                    if submit_reset:
                        if reset_code_input and new_password and confirm_new_password:
                            if new_password != confirm_new_password:
                                st.error("Passwords do not match.")
                            elif len(new_password) < 6:
                                st.error("Password must be at least 6 characters long.")
                            else:
                                if reset_password(st.session_state.reset_email, reset_code_input, new_password):
                                    st.success("Password reset successfully! You can now login with your new password.")
                                    st.session_state.reset_step = 1
                                    st.session_state.reset_email = ""
                                    st.session_state.reset_code = ""
                                    st.rerun()
                                else:
                                    st.error("Invalid reset code or failed to reset password.")
                        else:
                            st.error("Please fill in all fields.")
    
    else:
        # Main application for authenticated users
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.header("RAG Query System")
        
        with col2:
            if st.session_state.user_info:
                st.write(f"Welcome, {st.session_state.user_info['username']}")
            if st.button("Logout"):
                logout_user()
                st.rerun()
        
        # Chat interface
        st.subheader("Ask questions about company policies")
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("Chat History")
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.expander(f"Q{i+1}: {question[:50]}..."):
                    st.write(f"**Question:** {question}")
                    st.write(f"**Answer:** {answer}")
        
        # Query input
        with st.form("query_form"):
            question = st.text_area(
                "Enter your question:",
                placeholder="e.g., What is the company policy on remote work?",
                height=100
            )
            submit_query = st.form_submit_button("Ask Question")
            
            if submit_query and question.strip():
                with st.spinner("Processing your question..."):
                    answer = query_rag(question.strip())
                    
                    if answer:
                        st.success("Question processed successfully!")
                        
                        # Add to chat history
                        st.session_state.chat_history.append((question.strip(), answer))
                        
                        # Display current answer
                        st.subheader("Answer")
                        st.write(answer)
                        
                        # Keep only last 10 conversations
                        if len(st.session_state.chat_history) > 10:
                            st.session_state.chat_history = st.session_state.chat_history[-10:]
                    else:
                        st.error("Failed to get answer. Please try again.")
        
        # Clear chat history button
        if st.session_state.chat_history:
            if st.button("Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
        
        # User profile section
        with st.expander("User Profile"):
            if st.session_state.user_info:
                st.write(f"**User ID:** {st.session_state.user_info['id']}")
                st.write(f"**Email:** {st.session_state.user_info['email']}")
                st.write(f"**Username:** {st.session_state.user_info['username']}")
                st.write(f"**Account Created:** {st.session_state.user_info['created_at']}")

if __name__ == "__main__":
    main()
