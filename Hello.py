import streamlit as st

st.write("""
# FPL Mini League info
""")

league_id = st.text_input('Enter your league ID: ')
st.write('Your league id is: ', league_id)
