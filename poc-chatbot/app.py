import os
import streamlit as st
from dotenv import load_dotenv

# Load .env environment variables
load_dotenv()

from llm_translator import classify_intent, generate_cube_query, generate_context_answer
from cube_client import execute_cube_query
from schema_fetcher import fetch_cube_schema
from data_source_assistant import render_cube_selection_ui

CUBE_NAME = os.getenv("CUBE_NAME", "mrt_cbs_haltjongeren")
CUBEJS_API_SECRET = os.getenv("CUBEJS_API_SECRET")

# Establish session_states to remember input between runs
if "messages" not in st.session_state:
    st.session_state.messages = []

if "data_source_mode" not in st.session_state:
    st.session_state.data_source_mode = True  # Start in selection mode

if "selected_cube" not in st.session_state:
    st.session_state.selected_cube = None

if "selection_state" not in st.session_state:
    from data_source_assistant import DataSourceSelectionState
    st.session_state.selection_state = DataSourceSelectionState()

# Set up page layout with title and sidebar
st.set_page_config(page_title="Conversational Analytics POC", page_icon="🗣️")
st.title("Conversational Analytics")

with st.sidebar:
    st.header("Info")
    st.write("""
             
            This tool works in two layers: 

            **1. Searching for the most suitable datasource based on your description.**

            For example: *'I want to know more about Haltjongeren*."

            **2. Answering your questions based on the selected datasource.**

            Are you ready with the source? Click on 'Change datasource' on the bottom left. 
             """)
    st.header("Examples:")
    st.write("""
             - Which columns does this datasource contain? 
             - Give me a distinct of all values in the column delictgroep
             - How many Haltjongeren where there in 2024?
             - What are Haltjongeren?
             """)
    
    # Display selected cube if one is chosen
    if st.session_state.selected_cube:
        st.success(f"Active datasource: {st.session_state.selected_cube}")
        if st.button("Change datasource"):
            st.session_state.data_source_mode = True
            st.session_state.selection_state.start_selection()
            st.session_state.selected_cube = None
            st.rerun()

# Show the query and result from cube's request in json format 
def render_data_answer(cube_query, result):
    with st.expander("Generated cube request"):
        st.json(cube_query)
    with st.expander("Cube code"):
        st.json(result)

    rows = result.get("data", [])
    if not rows:
        st.write("No data has been found for this request.")
    elif len(rows) == 1 and len(rows[0]) == 1:
        value = list(rows[0].values())[0]
        st.metric(label="Result", value=value)
    else:
        st.table(rows)

# Create a chat mbubble for all input by user or the assistant
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            if message.get("type") == "data":
                render_data_answer(message["cube_query"], message["result"])
            else:
                # metadata or selection messages
                st.write(message["content"])
        else:
            st.write(message["content"])

# Select between datasource selection mode and query mode. Datasource selection is the starting point
if st.session_state.data_source_mode:
    if not st.session_state.selected_cube:

        if not st.session_state.selection_state.user_question:
            st.info(
                """
                #### Hey! 

                Describe the data that you are looking for briefly in the field underneath. 

                So far, only the datasources ***Haltjongeren*** and ***Verdachten*** are available. 

                Mind you, that this is a **proof of concept**, and not a tool ready for production. The product has been built with free-tier tools and might therefore not always work as expected. 

                If you get the error: `Error while loading: 502 Server Error: Bad Gateway for url`, click on [this link](https://poc-conversationalanalytics.onrender.com) and wait until it finishes loading. Then try again.

                Sometimes it takes a while for the data to be found. If the icon on the top right keeps changing, there is progress. 
                """
            )
        
        if user_question := st.chat_input(
            "Describe the data you are looking for..." 
        ):
            # Store user's description
            st.session_state.selection_state.set_question(user_question)
            st.session_state.messages.append({
                "role": "user",
                "content": user_question
            })
            
            with st.chat_message("user"):
                st.write(user_question)

        if st.session_state.selection_state.user_question and not st.session_state.selected_cube: 
            
            # Get available cubes W
            if "available_cubes" not in st.session_state:
                st.session_state.available_cubes = None

            if not st.session_state.available_cubes: 
                from data_source_selector import describe_all_cubes
                try:
                    st.session_state.available_cubes = describe_all_cubes()
                except Exception as e: 
                    st.session_state.available_cubes = []
                    st.error(f"Error while loading: {e}")
            
            # Render selection UI
            with st.chat_message("assistant"):
                st.write("Looking for your data..")

            selected = render_cube_selection_ui(
                st.session_state.selection_state.user_question,
                st.session_state.available_cubes
            )
                
            if selected:
                st.session_state.selected_cube = selected
                st.session_state.selection_state.set_selected_cube(selected)
                st.success(f"Gesecteerde bron: **{selected}**")
                
                # Add confirmation message
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "metadata",
                    "content": f"I selected '{selected}' as a datasource. What do you want to know about this data? "
                })
                
                # Switch to query mode automatically
                st.session_state.data_source_mode = False
                st.rerun()
            else:
                st.write("Select one of the datasources above.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "metadata",
                    "content": "Please select a datasource from the options above."
                })
    else:
        # Cube selected, prompt to switch to query mode
        st.info(f"You selected {st.session_state.selected_cube} as a datasource. You can now ask questions about the data and the context of the data source.")
        if st.button(f"Chat with {st.session_state.selected_cube}"):
            st.session_state.data_source_mode = False
            st.rerun()

else:

    
    # Use selected cube or fall back to default
    active_cube = st.session_state.selected_cube or CUBE_NAME
    st.caption(f"Actieve cube: `{active_cube}`")
    
    if user_question := st.chat_input("Ask your question about the data or the context"):
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                try:
                    intent = classify_intent(user_question)
                    st.caption(f"Detected intent: **{intent}**")

                    if intent == "metadata":
                        answer = generate_context_answer(user_question, active_cube)
                        st.write(answer)
                        st.session_state.messages.append(
                            {"role": "assistant", "type": "metadata", "content": answer}
                        )
                    else:
                        cube_query = generate_cube_query(user_question, active_cube)
                        result = execute_cube_query(cube_query)
                        render_data_answer(cube_query, result)
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "type": "data",
                                "content": "",
                                "cube_query": cube_query,
                                "result": result,
                            }
                        )
                except Exception as e:
                    error_text = f"Error: {e}"
                    st.error(error_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "type": "metadata", "content": error_text}
                    )
