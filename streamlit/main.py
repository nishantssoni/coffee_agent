import streamlit as st
import requests
import os


# Debugging information
# st.write("Debugging Information:")
# st.write(f"FASTAPI_URL environment variable: {os.getenv('FASTAPI_URL')}")
# st.write(f"Current working directory: {os.getcwd()}")
# st.write(f"List of environment variables: {dict(os.environ)}")

# --- Configuration ---
# Force the URL to use the service name instead of relying on environment variable
# --- Configuration ---
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://api:8000")  # Replace with your FastAPI URL
st.write(f"Using API URL: {FASTAPI_URL}")



# --- State Management ---
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

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
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Login failed: {e}")
        return False
    except requests.exceptions.HTTPError as e:
        st.error(f"Login failed: {response.json().get('detail', 'Invalid credentials')}")
        return False
    

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
            st.session_state['chat_history'] = [{"role": chat["role"], "content": chat["content"]} for chat in history_data]
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to load chat history: {e}")
        except requests.exceptions.HTTPError as e:
            st.error(f"Failed to load chat history: {response.json().get('detail', 'Something went wrong')}")

# --- UI ---
st.title("Chat App with JWT Authentication")

if not st.session_state['logged_in']:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(username, password)
else:
    with st.sidebar:
        st.write(f"Logged in as: {st.session_state['username']}")
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
                st.session_state['chat_history'].append({"role": "assistant", "content": response})
