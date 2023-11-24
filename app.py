import streamlit as st
from transformers import pipeline

# Load the fine-tuned model
pipe = pipeline("text-generation", model="Pontonkid/falcon-med")

def chatbot(conversation_history, user_input):
    # Add user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Generate assistant response
    with st.spinner('Thinking...'):
        assistant_response = pipe([item["content"] for item in conversation_history], max_length=100)[0]['generated_text']

    # Add assistant response to the conversation history
    conversation_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response, conversation_history

# Streamlit layout
st.title('Mental Health Chatbot')
st.sidebar.title('Chatbot Info')
st.sidebar.text('This chatbot is trained to assist with mental health concerns.')

# Initialize conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display conversation history on app rerun
for message in st.session_state.conversation_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.text_input('You:'):
    # Get assistant response and update conversation history using the chatbot function
    assistant_response, st.session_state.conversation_history = chatbot(st.session_state.conversation_history, user_input)
    
    # Display user input and assistant response in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
