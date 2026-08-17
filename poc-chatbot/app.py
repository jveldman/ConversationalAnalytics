import os
import streamlit as st
from dotenv import load_dotenv

# Load .env environment variables
load_dotenv()

from llm_translator import classify_intent, generate_cube_query, generate_context_answer
from cube_client import execute_cube_query
from schema_fetcher import fetch_cube_schema
from data_source_assistant import render_cube_selection_ui

CUBE_NAME = os.getenv("CUBE_NAME")
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
st.set_page_config(page_title="POC Conversational Analytics", page_icon="🗣️")
st.title("Conversational Analytics")

with st.sidebar:
    st.header("Informatie")
    st.write("""
             
            Deze tool werkt in twee stappen: 

            **1. Zoeken naar de meest geschikte databron op basis van je beschrijving.**

            Bijvoorbeeld: *'Ik wil meer weten over Haltjongeren'*.

            **2. Beantwoorden van je vragen op basis van de geselecteerde databron.**

            Ben je klaar met de bron? Klik dan links onderin op 'Databron wijzigen'. 
             """)
    st.header("Voorbeelden:")
    st.write("""
             - Welke kolommen bevat deze databron?
             - Geef mij een distinct van alle waarden in de kolom delictgroep
             - Hoeveel Haltjongeren waren er in 2024?
             - Wat zijn Haltjongeren?
             """)
    
    # Display selected cube if one is chosen
    if st.session_state.selected_cube:
        st.success(f"Actieve databron: {st.session_state.selected_cube}")
        if st.button("Databron wijzigen"):
            st.session_state.data_source_mode = True
            st.session_state.selection_state.start_selection()
            st.session_state.selected_cube = None
            st.rerun()

# Show the query and result from cube's request in json format 
def render_data_answer(cube_query, result):
    with st.expander("Gegenereerd Cube-verzoek"):
        st.json(cube_query)
    with st.expander("Cube-code"):
        st.json(result)

    rows = result.get("data", [])
    if not rows:
        st.write("Er zijn geen gegevens gevonden voor deze vraag.")
    elif len(rows) == 1 and len(rows[0]) == 1:
        value = list(rows[0].values())[0]
        st.metric(label="Resultaat", value=value)
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
                #### Hallo! 

                Beschrijf kort de gegevens die je zoekt in het veld hieronder. 

                Op dit moment zijn alleen de databronnen ***Haltjongeren*** en ***Verdachten*** beschikbaar. 

                Houd er rekening mee dat dit een **proof of concept** is en geen kant-en-klaar product. 

                Als je de foutmelding krijgt: `Fout bij laden: 502 Server Error: Bad Gateway for url`, klik dan op [deze link](https://poc-conversationalanalytics.onrender.com) en wacht tot de pagina volledig is geladen. Probeer het daarna opnieuw.

                Soms duurt het even voordat de gegevens zijn gevonden. Als het icoon rechtsboven blijft veranderen, is de tool nog bezig. 
                """
            )
        
        if user_question := st.chat_input(
            "Beschrijf de gegevens die je zoekt..." 
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
                    st.error(f"Fout bij laden: {e}")
            
            # Render selection UI
            with st.chat_message("assistant"):
                st.write("Op zoek naar je gegevens...")

            selected = render_cube_selection_ui(
                st.session_state.selection_state.user_question,
                st.session_state.available_cubes
            )
                
            if selected:
                st.session_state.selected_cube = selected
                st.session_state.selection_state.set_selected_cube(selected)
                st.success(f"Geselecteerde databron: **{selected}**")
                
                # Add confirmation message
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "metadata",
                    "content": f"Ik heb '{selected}' geselecteerd als databron. Wat wil je over deze gegevens weten? "
                })
                
                # Switch to query mode automatically
                st.session_state.data_source_mode = False
                st.rerun()
            else:
                st.write("Selecteer één van de databronnen hierboven.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "metadata",
                    "content": "Selecteer aub een databron uit de bovenstaande opties."
                })
    else:
        # Cube selected, prompt to switch to query mode
        st.info(f"Je hebt {st.session_state.selected_cube} geselecteerd als databron. Je kunt nu vragen stellen over de gegevens en de context van deze databron.")
        if st.button(f"Chat met {st.session_state.selected_cube}"):
            st.session_state.data_source_mode = False
            st.rerun()

else:

    
    # Use selected cube or fall back to default
    active_cube = st.session_state.selected_cube or CUBE_NAME or "default"
    st.caption(f"Actieve cube: `{active_cube}`")
    
    if user_question := st.chat_input("Stel je vraag over de gegevens of de context"):
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Zoeken..."):
                try:
                    intent = classify_intent(user_question)
                    st.caption(f"Gedetecteerde intentie: **{intent}**")

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
                    error_text = f"Fout: {e}"
                    st.error(error_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "type": "metadata", "content": error_text}
                    )
