import streamlit as st
import shelve
from assistant import ai

st.subheader("College Enguiry Chatbot")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

  
# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history_2") as db:
        return db.get("messages", [])
    
# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history_2") as db:
        db["messages"] = messages



# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()
    
school = st.sidebar.text_input(
            "Input the full name of the college", type="default",
        )
  
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])


def main() -> None:
    # Display chat messages
        for message in st.session_state.messages:
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                
        # Main chat interface
        if prompt := st.chat_input("How can I help?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(prompt)
                
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                reason = f"College Chatbot Getting information on {school}..."
                message_placeholder.markdown(reason + "|")
                message_placeholder.markdown(reason)
                full_response = ""
                full_response = ai(prompt=prompt, school=school)
                
                message_placeholder.markdown(full_response + "|")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save chat history after each interaction
        save_chat_history(st.session_state.messages)


main()