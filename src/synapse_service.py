import streamlit as st
import synapseclient
import pandas as pd

# Constants
TABLE_ID = "syn51476218"
EXCLUDED_SCHEMA_KEYS = ["id", "createdBy", "modifiedBy", "name", "etag"]


@st.cache_resource
def get_synapse_client(token):
    """Authenticate and return a Synapse client."""
    try:
        client = synapseclient.Synapse()
        client.login(authToken=token)
        return client
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None


@st.cache_data(ttl=600)
def fetch_project_list(_syn_client):
    """Query the Project View for ID and Name."""
    try:
        query = _syn_client.tableQuery(f"SELECT id, name FROM {TABLE_ID}")
        return query.asDataFrame()
    except Exception as e:
        st.error(f"Error querying table: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def fetch_view_schema(_syn_client):
    """Fetch the column names defined in the Project View Schema, excluding system cols."""
    try:
        columns = _syn_client.getTableColumns(TABLE_ID)
        return [col.name for col in columns if col.name not in EXCLUDED_SCHEMA_KEYS]
    except Exception as e:
        st.error(f"Error fetching schema: {e}")
        return []


def can_edit_entity(syn_client, entity_id):
    """Check if the user has EDIT permissions on an entity."""
    try:
        perms = syn_client.restGET(f"/entity/{entity_id}/permissions")
        return perms.get("canEdit", False)
    except Exception:
        return False


def fetch_wiki_headers(syn_client, project_id):
    """Get the tree of wiki pages for a project."""
    try:
        headers = syn_client.getWikiHeaders(project_id)
        return headers
    except Exception:
        return []


def fetch_wiki_page(syn_client, project_id, wiki_id):
    """Fetch a specific wiki page content."""
    try:
        return syn_client.getWiki(project_id, subpageId=wiki_id)
    except Exception as e:
        st.error(f"Could not load wiki page: {e}")
        return None


def fetch_project_folders(syn_client, project_id):
    """Get a list of folders within the project."""
    try:
        # getChildren returns a generator; convert to list
        return list(syn_client.getChildren(project_id, includeTypes=["folder"]))
    except Exception as e:
        st.warning(f"Could not fetch folders: {e}")
        return []


def fetch_folder_contents(syn_client, folder_id):
    """Get a list of files and sub-folders within a specific folder."""
    try:
        return list(syn_client.getChildren(folder_id, includeTypes=["file", "folder"]))
    except Exception:
        return []


def fetch_project_tables(syn_client, project_id):
    """Get a list of tables and views within the project."""
    try:
        return list(
            syn_client.getChildren(project_id, includeTypes=["table", "entityview"])
        )
    except Exception as e:
        st.warning(f"Could not fetch tables: {e}")
        return []


def update_annotation(syn_client, entity_id, key, value):
    """Update a specific annotation on an entity."""
    try:
        entity = syn_client.get(entity_id)
        # Synapse annotations are lists, so we wrap the value in a list
        entity.annotations[key] = [value]
        syn_client.store(entity)
        return True, f"✅ Successfully added annotation **{key}** to **{entity_id}**!"
    except Exception as e:
        return False, f"Failed to update annotation: {e}"
