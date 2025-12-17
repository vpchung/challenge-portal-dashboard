# Synapse Wiki Annotator

> [!NOTE]
> This project was created as part of the Sage Hackathon 2025, and may not be maintained moving forward.

A Streamlit dashboard for browsing and annotating Synapse projects, Wiki pages,
and folders for the [Challenge Portal](https://challenges.synapse.org/).

## Prerequisites

- Python 3.10 or higher
- A [Synapse account](https://www.synapse.org/)
- A Synapse Personal Access Token with appropriate permissions

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
   
   Then edit `.streamlit/secrets.toml` and add your Synapse Personal Access Token:
   ```toml
   SYNAPSE_AUTH_TOKEN = "your-actual-token-here"
   ```

   To create a Personal Access Token:
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

2. **Open your browser**:
   The app will automatically open at `http://localhost:8501`

3. **Log in**:
   - If you configured `secrets.toml`, you'll be automatically logged in
   - Otherwise, enter your Personal Access Token in the sidebar

4. **Explore and annotate**:
   - Select a project from the sidebar
   - Browse Wiki pages or folders
   - Add annotations using the form on the right

## Project Structure

```
challenge-portal-dashboard/
├── app.py                          # Home page - project selector and welcome
├── pages/                          # Multi-page app pages
│   └── 1_Project_Annotator.py     # Project annotation interface (self-contained)
├── src/                            # Source code package
│   ├── __init__.py                # Package initializer
│   ├── auth.py                    # Authentication utilities
│   └── synapse_service.py         # Synapse API interactions
├── .streamlit/                     # Streamlit configuration
│   ├── config.toml                # App theme and settings
│   ├── secrets.toml               # Authentication secrets (not in git)
│   └── secrets.toml.example       # Template for secrets file
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # License information
└── .gitignore                     # Git ignore rules
```

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

## Development

### Running in Development Mode

```bash
streamlit run app.py --server.runOnSave true
```

This enables auto-reload when you modify the code.

### Adding New Features

- **UI Components**: Add to `src/page_components.py`
- **Synapse API calls**: Add to `src/synapse_service.py`
- **New pages**: Create files in a `pages/` directory for multi-page apps

## Troubleshooting

### Authentication Issues

- Verify your token has the required scopes (`view`, `download`, `modify`)
- Check that `.streamlit/secrets.toml` exists and contains your token
- Ensure your token hasn't expired

### Project Not Loading

- Confirm you have access to the projects in Synapse
- Check that the table view ID is correct in `synapse_service.py`
- Verify network connectivity to Synapse servers

### Import Errors

- Ensure you're running from the project root directory
- Activate your virtual environment if using one
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/vpchung/challenge-portal-dashboard/issues)
- Check [Synapse documentation](https://help.synapse.org/)
- Review [Streamlit documentation](https://docs.streamlit.io/)

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web app framework
- [Synapse Python Client](https://python-docs.synapse.org/) - Synapse API wrapper
- [Pandas](https://pandas.pydata.org/) - Data manipulation