"""Authentication utilities for Synapse Wiki Annotator."""

import streamlit as st
from src import synapse_service as service


def require_auth():
    """
    Ensures user is authenticated. Gets token from secrets or shows error.
    Also displays the logged-in user info in the sidebar.

    Returns:
        synapseclient.Synapse: Authenticated Synapse client
    """
    if "SYNAPSE_AUTH_TOKEN" in st.secrets:
        auth_token = st.secrets["SYNAPSE_AUTH_TOKEN"]
    else:
        st.error(
            "🔐 Authentication token not found. Please configure `.streamlit/secrets.toml` with your SYNAPSE_AUTH_TOKEN."
        )
        st.stop()

    syn = service.get_synapse_client(auth_token)

    if not syn:
        st.error(
            "❌ Failed to authenticate with Synapse. Please check your token in `.streamlit/secrets.toml`."
        )
        st.stop()

    # Display logged-in user info in sidebar
    with st.sidebar:
        try:
            user_profile = syn.getUserProfile()
            username = user_profile.get("userName", "Unknown User")
            st.success(f"✅ Logged in as: **{username}**")
        except:
            st.info("👤 Logged in as **anonymous**")

    return syn
