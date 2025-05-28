import streamlit as st
import oci
import re
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SERVICE_ENDPOINT = os.getenv("OCI_SERVICE_ENDPOINT", "")
AGENT_ENDPOINT_ID = os.getenv("OCI_AGENT_ENDPOINT_ID", "")
PASSWORD_HASH = os.getenv("PASSWORD_HASH", "")
OS_URL = os.getenv("OS_URL", r"https://objectstorage\.eu-frankfurt-1\.oraclecloud\.com")
OS_URL_PREAUTH = os.getenv("OS_URL_PREAUTH", "")

# Page configuration
st.set_page_config(page_title="OCI GenAI Agents Demo", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False
if "oci_client" not in st.session_state:
    st.session_state.oci_client = None

# Preset questions
PRESET_QUESTIONS = [
    "Come si applica il principio della responsabilità estesa del produttore (EPR) nei settori degli imballaggi e dei RAEE?",
    "Quali sono i limiti di concentrazione per definire pericoloso un rifiuto contenente metalli pesanti e come si applicano i criteri HP?",
    "Un'azienda produce scarti di lavorazione metallica contaminati da oli. Quale procedura deve seguire per la classificazione e quali codici EER potrebbero applicarsi?",
    "Quali sono gli obblighi del produttore di rifiuti pericolosi che supera le 10 tonnellate annue secondo il SISTRI e le modifiche successive?",
    "Un laboratorio chimico deve smaltire reagenti scaduti di varia natura. Quali procedure deve seguire per il confezionamento, l'etichettatura e l'affidamento a trasportatori autorizzati?",
]

def check_password():
    """Handle password authentication"""
    def password_entered():
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == PASSWORD_HASH:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Handle logout
    if st.sidebar.button("🚪 Logout") and st.session_state.password_correct:
        st.session_state.password_correct = False
        st.session_state.messages = []
        st.session_state.oci_client = None
        st.rerun()

    if st.session_state.password_correct:
        return True

    # Login form
    st.title("🔐 Accesso Richiesto")
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    
    if st.session_state.get("password_correct") is False:
        st.error("Password errata. Riprova.")
    
    return False

def get_oci_client():
    """Initialize OCI client"""
    if st.session_state.oci_client is None:
        try:
            config = oci.config.from_file()
            st.session_state.oci_client = oci.generative_ai_agent_runtime.GenerativeAiAgentRuntimeClient(
                config, service_endpoint=SERVICE_ENDPOINT
            )
        except Exception as e:
            st.error(f"Failed to initialize OCI client: {e}")
            st.stop()
    return st.session_state.oci_client

def generate_response(user_message):
    """Generate response from OCI GenAI Agent"""
    client = get_oci_client()
    
    # Create session
    session_response = client.create_session(
        create_session_details=oci.generative_ai_agent_runtime.models.CreateSessionDetails(
            display_name="USER_Session", 
            description="User Session"
        ),
        agent_endpoint_id=AGENT_ENDPOINT_ID,
    )
    
    # Generate chat response
    chat_response = client.chat(
        agent_endpoint_id=AGENT_ENDPOINT_ID,
        chat_details=oci.generative_ai_agent_runtime.models.ChatDetails(
            user_message=user_message, 
            session_id=session_response.data.id
        ),
    )
    
    response_text = chat_response.data.message.content.text
    citations = extract_citations(chat_response.data.message.content)
    
    return response_text, citations

def extract_citations(content):
    """Extract citations from response content"""
    all_citations = []
    
    if hasattr(content, "citations") and content.citations:
        all_citations.extend(content.citations)
    
    if hasattr(content, "paragraph_citations") and content.paragraph_citations:
        for para_group in content.paragraph_citations:
            if hasattr(para_group, "citations") and para_group.citations:
                all_citations.extend(para_group.citations)
    
    # Remove duplicates
    unique_citations = []
    seen = set()
    for citation in all_citations:
        key = (getattr(citation, 'doc_id', ''), getattr(citation, 'title', ''))
        if key not in seen:
            unique_citations.append(citation)
            seen.add(key)
    
    return unique_citations

def format_citations(citations):
    """Format citations for display"""
    if not citations:
        return None

    citation_text = "**📚 Sources:**\n\n"
    
    for i, citation in enumerate(citations, 1):
        citation_text += f"**[{i}]** "
        
        if hasattr(citation, "title") and citation.title:
            citation_text += f"**{citation.title}**\n"
        
        if hasattr(citation, "page_numbers") and citation.page_numbers:
            pages = ", ".join(map(str, citation.page_numbers))
            citation_text += f"   📄 Page(s): {pages}\n"
        
        if hasattr(citation, "source_location") and citation.source_location:
            if hasattr(citation.source_location, "url") and citation.source_location.url:
                original_url = citation.source_location.url
                new_url = re.sub(OS_URL, OS_URL_PREAUTH, original_url)
                citation_text += f"   🔗 [View Source]({new_url})\n"
        
        citation_text += "\n"
    
    return citation_text

def main():
    # Check authentication
    if not check_password():
        return
    
    # Validate configuration
    if not AGENT_ENDPOINT_ID:
        st.error("OCI_AGENT_ENDPOINT_ID environment variable is required")
        return
    
    # Title
    st.title("🧠 OCI Generative AI Agents Demo")
    st.write("Assistente AI specializzato in normative ambientali e gestione rifiuti")
    
    # Sidebar with preset questions
    with st.sidebar:
        st.header("🎯 Domande Rapide")
        
        for i, question in enumerate(PRESET_QUESTIONS):
            if st.button(question[:60] + "...", key=f"preset_{i}", help=question):
                st.session_state.messages.append({"role": "user", "content": question})
                
                with st.spinner("Generando risposta..."):
                    try:
                        response_text, citations = generate_response(question)
                        formatted_citations = format_citations(citations)
                        
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response_text,
                            "citations": formatted_citations
                        })
                    except Exception as e:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"Errore: {e}",
                            "citations": None
                        })
                
                st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            if message["role"] == "assistant" and message.get("citations"):
                with st.expander("📚 Visualizza Sources"):
                    st.markdown(message["citations"])
    
    # Chat input
    if prompt := st.chat_input("Come posso aiutarti?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Generando risposta..."):
                try:
                    response_text, citations = generate_response(prompt)
                    st.write(response_text)
                    
                    formatted_citations = format_citations(citations)
                    if formatted_citations:
                        with st.expander("📚 Visualizza Sources"):
                            st.markdown(formatted_citations)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text,
                        "citations": formatted_citations
                    })
                    
                except Exception as e:
                    error_msg = f"Errore: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "citations": None
                    })

if __name__ == "__main__":
    main()