import streamlit as st
import requests
import os
import json

# --- Configuration ---
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://api:8000")  # Replace with your FastAPI URL

# --- State Management ---
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'last_order' not in st.session_state:
    st.session_state['last_order'] = None
if 'show_register' not in st.session_state:
    st.session_state['show_register'] = False

# --- Authentication Functions ---
def login(username, password):
    login_data = {"username": username, "password": password}
    try:
        response = requests.post(f"{FASTAPI_URL}/auth/login", data=login_data)
        response.raise_for_status()  # Raise an exception for bad status codes
        token_data = response.json()
        st.session_state['jwt_token'] = token_data.get("access_token")
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.success("Logged in successfully!")
        load_chat_history()
        st.rerun()
        load_chat_history()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Login failed: {e}")
        return False
    except requests.exceptions.HTTPError as e:
        st.error(f"Login failed: {response.json().get('detail', 'Invalid credentials')}")
        return False
    
def register_user(username, email, password):
    register_data = {
        "username": username,
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{FASTAPI_URL}/users/", json=register_data)
        response.raise_for_status()
        st.success("Registration successful! You can now log in.")
        st.session_state['show_register'] = False
        return True
    except requests.exceptions.HTTPError as e:
        error_detail = "Registration failed"
        try:
            error_json = response.json()
            if 'detail' in error_json:
                error_detail = error_json['detail']
        except:
            pass
        st.error(f"{error_detail}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Registration failed: {e}")
        return False

def toggle_register_form():
    st.session_state['show_register'] = not st.session_state['show_register']
    st.rerun()

def logout():
    st.session_state['jwt_token'] = None
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['chat_history'] = []
    st.info("Logged out.")
    st.rerun()

def get_chat_response(prompt):
    if not st.session_state['jwt_token']:
        st.error("Please log in to chat.")
        return None

    headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}
    payload = {"prompt": prompt}
    try:
        response = requests.post(f"{FASTAPI_URL}/chats/ask", headers=headers, json=payload)
        response.raise_for_status()
        chat_response = response.json()
        return chat_response.get("content")
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending message: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"Error sending message: {response.json().get('detail', 'Something went wrong')}")
        return None

def load_chat_history():
    if st.session_state['logged_in'] and st.session_state['jwt_token']:
        headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}
        try:
            response = requests.get(f"{FASTAPI_URL}/chats/history", headers=headers)
            response.raise_for_status()
            history_data = response.json()
            # Store last order in session state
            st.session_state['last_order'] = get_last_order_from_memory(history_data)
            st.session_state['chat_history'] = [{"role": chat["role"], "content": chat["content"]} for chat in history_data]
        
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to load chat history: {e}")
        except requests.exceptions.HTTPError as e:
            st.error(f"Failed to load chat history: {response.json().get('detail', 'Something went wrong')}")

def get_last_order_from_memory(data):
    """Extract the most recent non-empty order from chat memory field."""
    for message in reversed(data):
        memory = message.get("memory", {})
        if (
            isinstance(memory, dict)
            and memory.get("agent") == "order_taking_agent"
            and memory.get("order")  # Ensures order exists and is not empty
        ):
            return memory["order"]
    return []

# --- UI --
st.title("Order Coffee from Bot")

if not st.session_state['logged_in']:
    if st.session_state['show_register']:
        with st.form("register_form"):
            st.subheader("Create New Account")
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                back_button = st.form_submit_button("Back to Login")
            with col2:
                register_button = st.form_submit_button("Register")
            
            if register_button:
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif not new_username or not new_email or not new_password:
                    st.error("All fields are required")
                else:
                    register_user(new_username, new_email, new_password)
            
            if back_button:
                st.session_state['show_register'] = False
                st.rerun()
    else:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Login")
            with col2:
                register_link = st.form_submit_button("Create Account")
            
            if submitted and username and password:
                login(username, password)
                
            if register_link:
                st.session_state['show_register'] = True
                st.rerun()
else:
    with st.sidebar:
        st.write(f"Logged in as: {st.session_state['username']}")
        
        if st.session_state.get("last_order"):
            st.sidebar.markdown("### 🛒 Last Order")
            for item in st.session_state["last_order"]:
                st.sidebar.write(f"{item['quantity']}x {item['item']} ({item['price']})")
        else:
            st.sidebar.info("No recent orders found.")

        if st.button("Logout"):
            logout()

    st.subheader("Chat History")
    for message in st.session_state['chat_history']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Say something")
    if prompt:
        st.session_state['chat_history'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chat_response(prompt)
            if response:
                st.markdown(response)
                load_chat_history()
                st.rerun()