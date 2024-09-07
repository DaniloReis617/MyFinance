import streamlit as st

def contact_form():
    st.title("Contact Me")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Send"):
        # Lógica para enviar a mensagem
        st.success("Message sent successfully!")
