"""Challenge Portal Annotator - Browse and annotate Synapse challenge projects."""

import streamlit as st
import pandas as pd
from src import auth, synapse_service as service

# ------------------------------------------------------------------
# 1. Config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Challenge Portal Annotator",
    layout="wide",
    page_icon="🏆",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# 2. Custom CSS
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# 3. Authentication
# ------------------------------------------------------------------
syn = auth.require_auth()

# Initialize Session State
if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None
if "selected_project_name" not in st.session_state:
    st.session_state.selected_project_name = None


# ------------------------------------------------------------------
# Helper: Cached function to fetch project data with annotations
# ------------------------------------------------------------------
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_projects_with_annotations(_syn):
    """Fetch all projects with their annotations status and permissions."""
    projects_df = service.fetch_project_list(_syn)

    if projects_df.empty:
        return []

    table_data = []
    for _, row in projects_df.iterrows():
        project_id = row["id"]
        project_name = row["name"]

        # Check if any annotations exist (excluding system annotations)
        has_annotations = False
        try:
            annos = _syn.get_annotations(project_id)
            # Check if there are any non-empty annotations
            if annos:
                has_annotations = any(annos.get(key) for key in annos.keys())
        except:
            has_annotations = False

        # Check edit permissions
        can_edit = service.can_edit_entity(_syn, project_id)

        table_data.append(
            {
                "Project Name": project_name,
                "Project ID": project_id,
                "Has Annotations": has_annotations,
                "Can Edit": can_edit,
            }
        )

    return table_data


# ------------------------------------------------------------------
# 4. Project Table View (if not selected)
# ------------------------------------------------------------------
if st.session_state.selected_project_id is None:
    st.title("🏆 Challenge Projects")
    st.markdown("View and annotate challenge projects for the Challenge Portal")
    st.caption(":orange[🔗 Link to portal: https://challenges.synapse.org/]")

    # Add refresh button to clear cache
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh", help="Reload project data"):
            fetch_projects_with_annotations.clear()
            st.rerun()

    st.markdown("---")

    with st.spinner("Loading challenge projects..."):
        all_projects = fetch_projects_with_annotations(syn)

    if all_projects:
        # Create searchable/filterable project list
        search = st.text_input(
            "🔍 Search challenge projects", placeholder="Type to filter..."
        )

        # Filter projects based on search
        if search:
            table_data = [
                p
                for p in all_projects
                if search.lower() in p["Project Name"].lower()
                or search.lower() in p["Project ID"].lower()
            ]
        else:
            table_data = all_projects

        if not table_data:
            st.warning("No challenge projects match your search.")
        else:
            st.markdown(f"*Showing {len(table_data)} project(s)*")

            # Create table display
            for item in table_data:
                col1, col2, col3, col4 = st.columns([3, 2, 1.5, 1])

                with col1:
                    st.markdown(f"**{item['Project Name']}**")

                with col2:
                    st.caption(item["Project ID"])

                with col3:
                    if item["Has Annotations"]:
                        st.markdown(
                            "✅ <span style='color: #28a745;'>Has annotations</span>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            "❌ <span style='color: #dc3545;'>No annotations</span>",
                            unsafe_allow_html=True,
                        )

                with col4:
                    if item["Can Edit"]:
                        if st.button(
                            "Annotate",
                            key=f"annotate_{item['Project ID']}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_project_id = item["Project ID"]
                            st.session_state.selected_project_name = item[
                                "Project Name"
                            ]
                            st.rerun()
                    else:
                        st.markdown("🔒", help="No edit permission")

                st.divider()
    else:
        st.warning(
            "No challenge projects found. Make sure you have access to at least one Synapse challenge project."
        )

    st.stop()

# ------------------------------------------------------------------
# 5. Page Header (when project is selected)
# ------------------------------------------------------------------
project_id = st.session_state.selected_project_id
project_name = st.session_state.selected_project_name

st.title(f"📖 {project_name}")
st.caption(f"Synapse Project ID: {project_id}")

# Check for and display persistent success/error messages (from previous rerun)
if "annotation_msg" in st.session_state:
    msg_type, msg_text = st.session_state.annotation_msg
    if msg_type == "success":
        st.success(msg_text, icon="✅")
    elif msg_type == "error":
        st.error(msg_text, icon="❌")
    # Clear message so it doesn't persist forever
    del st.session_state.annotation_msg

# ------------------------------------------------------------------
# 6. Sidebar: Project Navigation
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("---")

    # Search bar for quick project search
    project_search = st.text_input(
        "🔍 Search Projects",
        placeholder="Type to search...",
        key="sidebar_project_search",
    )

    # Button to clear selection and return to project list
    if st.button("📂 List All Challenge Projects", use_container_width=True):
        st.session_state.selected_project_id = None
        st.session_state.selected_project_name = None
        st.rerun()

    st.markdown("---")

    # Collapsible switcher using Radio buttons
    with st.expander("🔄 Project Quick Switch", expanded=False):
        with st.spinner("Loading..."):
            # Use cached data to get projects with permissions
            all_projects = fetch_projects_with_annotations(syn)

            # Filter to only editable projects
            editable_projects = [p for p in all_projects if p["Can Edit"]]

        if editable_projects:
            # Filter projects based on search
            if project_search:
                filtered_projects = [
                    p
                    for p in editable_projects
                    if project_search.lower() in p["Project Name"].lower()
                    or project_search.lower() in p["Project ID"].lower()
                ]
            else:
                filtered_projects = editable_projects

            if not filtered_projects:
                st.warning("No projects match your search.")
            else:
                project_options = {
                    f"{p['Project Name']} ({p['Project ID']})": p["Project ID"]
                    for p in filtered_projects
                }

                current_label = next(
                    (k for k, v in project_options.items() if v == project_id), None
                )

                # Only set default index if current project is in filtered results
                if current_label:
                    default_index = list(project_options.keys()).index(current_label)
                else:
                    default_index = 0

                new_selection_label = st.radio(
                    "Select Project:",
                    options=project_options.keys(),
                    index=default_index,
                    key="project_switcher_radio",
                )

                new_id = project_options[new_selection_label]
                if new_id != project_id:
                    st.session_state.selected_project_id = new_id
                    clean_name = new_selection_label.split(" (syn")[0]
                    st.session_state.selected_project_name = clean_name
                    st.rerun()  # Stay on same page, just refresh with new project
        else:
            st.warning("No projects with edit permissions found.")

# ------------------------------------------------------------------
# 7. Permission Check
# ------------------------------------------------------------------
can_edit = service.can_edit_entity(syn, project_id)

if not can_edit:
    st.error("🔒 You do not have permission to edit annotations for this project.")
    st.info(
        "Wiki pages and folders are hidden for read-only projects. Please select a different project from the sidebar."
    )
    st.stop()

# ------------------------------------------------------------------
# 8. Sidebar: Resource Navigation
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    resource_type = st.radio(
        "Select Resource Type:", ["Wiki Pages", "Folders", "Tables"]
    )

    selected_item_id = None
    selected_item_title = None

    if resource_type == "Wiki Pages":
        wiki_headers = service.fetch_wiki_headers(syn, project_id)
        if not wiki_headers:
            st.warning("No Wiki pages found.")
        else:
            wiki_map = {h["title"]: h["id"] for h in wiki_headers}
            selected_item_title = st.radio("Select Wiki Page:", options=wiki_map.keys())
            selected_item_id = wiki_map[selected_item_title]

    elif resource_type == "Folders":
        folders = service.fetch_project_folders(syn, project_id)
        if not folders:
            st.warning("No folders found.")
        else:
            folder_map = {f"{f['name']} ({f['id']})": f["id"] for f in folders}
            selected_item_title = st.radio("Select Folder:", options=folder_map.keys())
            selected_item_id = folder_map[selected_item_title]

    elif resource_type == "Tables":
        tables = service.fetch_project_tables(syn, project_id)
        if not tables:
            st.warning("No tables found.")
        else:
            table_map = {f"{t['name']} ({t['id']})": t["id"] for t in tables}
            selected_item_title = st.radio("Select Table:", options=table_map.keys())
            selected_item_id = table_map[selected_item_title]

# ------------------------------------------------------------------
# 9. Main Content
# ------------------------------------------------------------------
if not selected_item_id:
    st.info("Select an item from the sidebar to view details.")
    st.stop()

left_col, right_col = st.columns([2, 1], gap="medium")

default_anno_key = "documentationLink"
default_anno_val = ""
form_help_text = ""

# --- RENDER CONTENT ---
with left_col:
    if resource_type == "Wiki Pages":
        with st.spinner("Loading content..."):
            wiki_page = service.fetch_wiki_page(syn, project_id, selected_item_id)

        if wiki_page:
            st.header(wiki_page.title)
            st.markdown("---")
            st.markdown(wiki_page.markdown)

            default_anno_val = f"{project_id}/wiki/{selected_item_id}"
            form_help_text = "Link this Wiki page to the Project."
        else:
            st.error("Wiki page content could not be loaded.")
            st.stop()

    elif resource_type == "Folders":
        st.subheader(f"Folder: {selected_item_title}")
        st.markdown(f"**Synapse ID:** `{selected_item_id}`")
        st.markdown(
            f"[View on Synapse Web](https://www.synapse.org/Synapse:{selected_item_id})"
        )

        # --- Check for Folder Wiki (README) ---
        folder_wiki_headers = service.fetch_wiki_headers(syn, selected_item_id)
        if folder_wiki_headers:
            with st.expander("📖 Folder Wiki", expanded=True):
                with st.spinner("Loading folder wiki..."):
                    folder_wiki = service.fetch_wiki_page(syn, selected_item_id, None)
                    if folder_wiki:
                        st.markdown(folder_wiki.markdown)

        st.divider()
        st.markdown("### 📂 Folder Contents")
        with st.spinner("Fetching contents..."):
            folder_contents = service.fetch_folder_contents(syn, selected_item_id)

        if folder_contents:
            content_data = []
            for item in folder_contents:
                # Check type for icon
                is_folder = "Folder" in item.get("type", "")
                icon = "📂" if is_folder else "📄"

                content_data.append(
                    {
                        "": icon,
                        "Name": item.get("name", "Unknown"),
                        "ID": item.get("id", "Unknown"),
                        "Created": item.get("createdOn", "Unknown"),
                    }
                )

            st.dataframe(
                pd.DataFrame(content_data), use_container_width=True, hide_index=True
            )
        else:
            st.info("This folder is empty.")

        default_anno_key = "DataFolder"
        default_anno_val = selected_item_id
        form_help_text = "Link this Folder to the Project."

    elif resource_type == "Tables":
        st.subheader(f"Table: {selected_item_title}")
        st.markdown(f"**Synapse ID:** `{selected_item_id}`")
        st.markdown(
            f"[View on Synapse Web](https://www.synapse.org/Synapse:{selected_item_id})"
        )

        # Currently just showing basic info, but could be expanded to show columns or query data
        st.info("Select this table to annotate it as a challenge resource.")

        default_anno_key = "ChallengeTable"
        default_anno_val = selected_item_id
        form_help_text = "Link this Table to the Project."

# --- RENDER ANNOTATION FORM ---
with right_col:
    st.markdown("### 🏷️ Set Annotation")
    st.info(form_help_text)

    with st.container(border=True):
        # Fetch Schema Columns
        schema_columns = list(
            service.fetch_view_schema(syn)
        )  # Make a copy to modify safely

        # Prioritize 'status' in the list
        if "status" in schema_columns:
            schema_columns.remove("status")
            schema_columns.insert(0, "status")

        # --- SELECT KEY ---
        if schema_columns:
            default_idx = 0
            if default_anno_key in schema_columns:
                default_idx = schema_columns.index(default_anno_key)
            elif (
                resource_type == "Wiki Pages" and "documentationLink" in schema_columns
            ):
                default_idx = schema_columns.index("documentationLink")

            anno_key = st.selectbox(
                "Annotation Key", options=schema_columns, index=default_idx
            )
        else:
            anno_key = st.text_input("Annotation Key", value=default_anno_key)

        # --- DISPLAY CURRENT VALUE (Dynamic Placeholder) ---
        current_value_placeholder = st.empty()

        def update_current_value_display():
            try:
                current_annos = syn.get_annotations(project_id)
                current_val_raw = current_annos.get(anno_key)

                if current_val_raw:
                    if isinstance(current_val_raw, list):
                        current_val_display = ", ".join(map(str, current_val_raw))
                    else:
                        current_val_display = str(current_val_raw)
                else:
                    current_val_display = "(empty)"

                current_value_placeholder.markdown(
                    f"""
                    <div style="background-color: #f0f2f6; padding: 12px; border-radius: 8px; border-left: 4px solid #1f77b4; margin-bottom: 16px;">
                        <p style="margin: 0; font-size: 13px; color: #666; font-weight: 500;">CURRENT VALUE</p>
                        <p style="margin: 8px 0 0 0; font-size: 18px; color: #262730; font-weight: 600;">{current_val_display}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception:
                current_value_placeholder.markdown(
                    f"""
                    <div style="background-color: #fff3cd; padding: 12px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 16px;">
                        <p style="margin: 0; font-size: 13px; color: #856404; font-weight: 500;">CURRENT VALUE</p>
                        <p style="margin: 8px 0 0 0; font-size: 16px; color: #856404; font-style: italic;">Could not fetch</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        update_current_value_display()

        # --- INPUT VALUE ---
        with st.form("annotation_form"):

            if anno_key and anno_key.lower() == "status":
                anno_value = st.selectbox(
                    "New Status", options=["Active", "Upcoming", "Closed"]
                )
            elif anno_key and anno_key.lower() == "challengetype":
                challenge_types = st.multiselect(
                    "Challenge Type(s)",
                    options=["Data To Model", "Model to Data", "Project/Writeup"],
                    help="Select one or more challenge types",
                )
                # Convert list to comma-separated string for annotation
                anno_value = ", ".join(challenge_types) if challenge_types else ""
            else:
                anno_value = st.text_input("New Value", value=default_anno_val)

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "💾 Save Annotation", use_container_width=True
            )

            if submitted:
                with st.spinner("Saving annotation..."):
                    success, message = service.update_annotation(
                        syn, project_id, anno_key, anno_value
                    )

                if success:
                    st.success(message)
                    update_current_value_display()
                else:
                    st.error(message)
