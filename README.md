<div align="center">
   
   # Challenge Annotator
   
   ### Streamlit dashboard for annotating [Challenge Portal](https://challenges.synapse.org/) challenges

</div>

> [!NOTE]
> This project was created as part of the Sage Hackathon 2025, and may not be maintained moving forward.

### Prerequisites

- Python 3.10 or higher
- [Synapse account](https://www.synapse.org/)
- Synapse Personal Access Token (PAT) with appropriate permissions

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vpchung/challenge-portal-dashboard.git
   cd challenge-portal-dashboard
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Synapse authentication**:
   
   Create a `.streamlit/secrets.toml` file in the project root:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   
   Then edit `.streamlit/secrets.toml` and add your Synapse PAT:
   ```toml
   SYNAPSE_AUTH_TOKEN = "your-actual-token-here"
   ```

   To create a PAT:
   - Log in to [Synapse](https://www.synapse.org/)
   - Go to Settings → Personal Access Tokens
   - Click "Create New Token"
   - Select scopes: `view`, `download`, `modify`
   - Copy the token and paste it in your `secrets.toml`

## Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

   To run in development mode:

   ```bash
   streamlit run app.py --server.runOnSave true
   ```

3. **Open your browser**:
   The app will automatically open at `http://localhost:8501`

4. **Log in**:
   - If you configured `secrets.toml`, you'll be automatically logged in
   - Otherwise, enter your Personal Access Token in the sidebar

5. **Explore and annotate**:
   - Select a project from the sidebar
   - Browse Wiki pages or folders
   - Add annotations using the form on the right

## Configuration

### Theme Customization

Edit `.streamlit/config.toml` to customize the app's appearance:

```toml
[theme]
primaryColor = "#FF6B6B"       # Primary accent color
backgroundColor = "#FFFFFF"     # Main background
secondaryBackgroundColor = "#F0F2F6"  # Sidebar background
textColor = "#262730"          # Text color
font = "sans serif"            # Font family
```

### Synapse Table Configuration

The app queries a specific Synapse table view (default: `syn51476218`). To use a different table:

1. Open `src/synapse_service.py`
2. Update the `TABLE_ID` constant:
   ```python
   TABLE_ID = "syn12345678"  # Your table ID
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web app framework
- [Synapse Python Client](https://python-docs.synapse.org/) - Synapse API wrapper
- [Pandas](https://pandas.pydata.org/) - Data manipulation
