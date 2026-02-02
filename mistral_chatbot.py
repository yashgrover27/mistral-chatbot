# ============================================
# MISTRAL AI CHATBOT - STREAMLIT APP
# ============================================
# This is a simple chatbot that talks to you using Mistral AI
# Every line has a comment to help you understand what it does!

# --------------------------------------------
# STEP 1: Import Libraries (Bring in tools we need)
# --------------------------------------------

import streamlit as st
# 'streamlit' is like a toolbox that helps us create websites easily
# We nickname it 'st' so we don't have to type 'streamlit' every time

import requests
# 'requests' helps our program talk to the internet
# We use it to send messages to Mistral AI and get responses back

import json
# 'json' helps us organize data in a format that computers understand
# It's like putting things in labeled boxes

# --------------------------------------------
# STEP 2: Set Up the Page (Make it look nice)
# --------------------------------------------

st.set_page_config(
    page_title="Mistral AI Chatbot",  # This is the name shown in your browser tab
    page_icon="🤖",  # This is the little icon in your browser tab
    layout="centered"  # This makes everything appear in the center of the page
)

# --------------------------------------------
# STEP 3: Add a Title (The heading of our page)
# --------------------------------------------

st.title("🤖 Mistral AI Chatbot")
# This creates a big heading at the top of the page

st.markdown("*Your friendly AI assistant powered by Mistral AI*")
# This adds a smaller subtitle below the title (the * makes it italic)

# --------------------------------------------
# STEP 4: Create a Sidebar (Side menu for settings)
# --------------------------------------------

with st.sidebar:
    # Everything inside this block will appear in the sidebar on the left
    
    st.header("⚙️ Settings")
    # Creates a heading in the sidebar
    
    api_key = st.text_input(
        "Enter your Mistral API Key:", 
        type="password"
    )
    # This creates a password box where you type your API key
    # type="password" means the text will be hidden (shown as dots)
    # We save what you type in a variable called 'api_key'
    
    st.markdown("---")
    # This creates a horizontal line to separate sections
    
    st.markdown("### 📚 How to get your API Key:")
    # Creates a smaller heading
    
    st.markdown("""
    1. Go to [Mistral AI Console](https://console.mistral.ai/)
    2. Sign up or log in
    3. Go to 'API Keys' section
    4. Click 'Create new key'
    5. Copy the key and paste it above
    """)
    # This creates a numbered list of instructions
    # The triple quotes """ let us write multiple lines
    
    st.markdown("---")
    # Another horizontal line
    
    # Add a button to clear the chat
    if st.button("🗑️ Clear Chat History"):
        # This creates a clickable button
        # The 'if' means: "if someone clicks this button, do the following:"
        
        st.session_state.messages = []
        # This empties our chat history (like erasing a whiteboard)
        
        st.rerun()
        # This refreshes the page to show the empty chat

# --------------------------------------------
# STEP 5: Initialize Chat History (Set up memory)
# --------------------------------------------

if "messages" not in st.session_state:
    # This checks: "Do we already have a chat history saved?"
    # st.session_state is like the app's memory
    
    st.session_state.messages = []
    # If we don't have a chat history, create an empty one
    # [] means an empty list (like an empty shopping list)

# --------------------------------------------
# STEP 6: Display Previous Messages (Show old conversation)
# --------------------------------------------

for message in st.session_state.messages:
    # This goes through each message we saved before
    # It's like reading through your text message history
    
    with st.chat_message(message["role"]):
        # This creates a chat bubble
        # message["role"] tells us if it's from "user" or "assistant"
        
        st.markdown(message["content"])
        # This displays the actual message text inside the bubble

# --------------------------------------------
# STEP 7: Define Function to Call Mistral AI
# --------------------------------------------

def get_mistral_response(messages, api_key):
    """
    This function sends your messages to Mistral AI and gets a response back
    
    Think of it like:
    - You write a letter (messages)
    - You put it in an envelope with a stamp (api_key)
    - You send it to Mistral AI
    - They read it and write back
    """
    
    # The URL where Mistral AI lives on the internet
    url = "https://api.mistral.ai/v1/chat/completions"
    
    # The headers are like the envelope for our letter
    # They tell Mistral who we are and what we're sending
    headers = {
        "Content-Type": "application/json",  # We're sending JSON data
        "Authorization": f"Bearer {api_key}"  # This is our API key (like a password)
    }
    
    # The payload is the actual letter we're sending
    # It contains all our messages and settings
    payload = {
        "model": "mistral-small-latest",  # Which AI brain to use
        "messages": messages,  # All our conversation so far
        "temperature": 0.7,  # How creative the AI should be (0-1, higher = more creative)
        "max_tokens": 1000  # Maximum length of response (like a word limit)
    }
    
    try:
        # 'try' means: "Try to do this, but if something goes wrong, don't crash!"
        
        # Send our request to Mistral AI
        response = requests.post(url, headers=headers, json=payload)
        # 'post' means we're sending data (like mailing a letter)
        
        # Check if it worked
        response.raise_for_status()
        # This will give an error if something went wrong
        
        # Get the AI's reply from the response
        result = response.json()
        # Convert the response to a format we can use
        
        # Extract just the text of the reply
        assistant_message = result['choices'][0]['message']['content']
        # This digs into the response to find the actual message text
        
        return assistant_message
        # Send back the AI's reply
        
    except requests.exceptions.RequestException as e:
        # If something went wrong, we end up here
        
        return f"❌ Error: {str(e)}\n\nPlease check your API key and try again."
        # Return an error message to show the user

# --------------------------------------------
# STEP 8: Handle User Input (Chat Box at Bottom)
# --------------------------------------------

if prompt := st.chat_input("Type your message here..."):
    # This creates a chat input box at the bottom
    # 'prompt' will contain whatever you type
    # The ':=' is a special way to both check if something exists AND save it
    
    # --------------------------------------------
    # Check if API key is entered
    # --------------------------------------------
    
    if not api_key:
        # 'not' means "if this is empty or missing"
        
        st.error("⚠️ Please enter your Mistral API key in the sidebar first!")
        # Show an error message in red
        
        st.stop()
        # Stop here and don't continue
    
    # --------------------------------------------
    # Save and display user's message
    # --------------------------------------------
    
    # Add what you typed to the chat history
    st.session_state.messages.append({
        "role": "user",  # This message is from you
        "content": prompt  # This is what you typed
    })
    # 'append' means "add to the end of the list"
    
    # Display your message in a chat bubble
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # --------------------------------------------
    # Get AI response and display it
    # --------------------------------------------
    
    # Create a chat bubble for the AI's response
    with st.chat_message("assistant"):
        
        # Create a placeholder where we'll show the response
        message_placeholder = st.empty()
        
        # Show a "thinking" message while we wait
        with st.spinner("🤔 Thinking..."):
            
            # Call our function to get Mistral AI's response
            full_response = get_mistral_response(
                st.session_state.messages,  # Send all our conversation
                api_key  # Send our API key
            )
        
        # Display the AI's response
        message_placeholder.markdown(full_response)
    
    # --------------------------------------------
    # Save AI's response to chat history
    # --------------------------------------------
    
    st.session_state.messages.append({
        "role": "assistant",  # This message is from the AI
        "content": full_response  # This is what the AI said
    })

# --------------------------------------------
# STEP 9: Add Instructions at the Bottom
# --------------------------------------------

st.markdown("---")
# Horizontal line to separate sections

st.markdown("""
### 💡 Tips:
- Type your question in the chat box at the bottom
- Press Enter to send
- The AI will respond to you
- Click 'Clear Chat History' in the sidebar to start fresh
""")
