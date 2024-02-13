from google.cloud import dialogflow_v2beta1 as dialogflow
import streamlit as st
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Sigrid.json'

project_id = 'sigrid-mmvf'
session_id = '12345'
language_code = 'en'

session_client = dialogflow.SessionsClient()

def detect_intent_text(text):
	session = session_client.session_path(project_id, session_id)
	text_input = dialogflow.TextInput(text=text, language_code=language_code)
	query_input = dialogflow.QueryInput(text=text_input)

	response = session_client.detect_intent(request= {'session': session, 'query_input': query_input})

	return response.query_result.fulfillment_text


st.title('CHATBOT')

if 'messages' not in st.session_state:
	st.session_state.messages = []

for message in st.session_state.messages:
	display_input = st.chat_message(message['role'])
	display_input.write(message['content'])

prompt = st.chat_input('You: ')
if prompt:
	st.chat_message('user').write(prompt)

	st.session_state.messages.append({'role': 'user', 'content': prompt})

	bot_response = detect_intent_text(prompt)

	st.chat_message('assistant').write(bot_response)

	st.session_state.messages.append({'role': 'assistant', 'content': bot_response})