# OCI GenAI Agents Demo

A Streamlit application that provides an AI assistant specialized in environmental regulations and waste management, powered by Oracle Cloud Infrastructure (OCI) Generative AI Agents.

## Features

- 🔐 **Secure Authentication** - Password-protected access with SHA256 hashing
- 🧠 **AI-Powered Chat** - Interactive chat interface with OCI GenAI Agent
- 🎯 **Preset Questions** - Quick access to common environmental regulation queries
- 📚 **Source Citations** - Automatic citation extraction and formatting
- 💬 **Chat History** - Persistent conversation history during session
- 🌐 **Document Access** - Direct links to source documents

## Prerequisites

- Python 3.8 or higher
- Oracle Cloud Infrastructure (OCI) account
- OCI GenAI Agent configured and deployed

## Installation

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd oci-genai-demo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit oci python-dotenv
   ```

## Configuration

### 1. OCI Configuration

Create an OCI configuration file at `~/.oci/config`:

```ini
[DEFAULT]
user=ocid1.user.oc1..your-user-ocid
fingerprint=your-fingerprint
tenancy=ocid1.tenancy.oc1..your-tenancy-ocid
region=eu-frankfurt-1
key_file=~/.oci/your-private-key.pem
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
# All variables are required
OCI_AGENT_ENDPOINT_ID=your-agent-endpoint-id
OCI_SERVICE_ENDPOINT=https://agent-runtime.generativeai.eu-frankfurt-1.oci.oraclecloud.com
PASSWORD_HASH=3b244014b6229197d7b7555af9d57bee3c7eb74392ce2d4314cd74945c3c9b72
OS_URL=https://objectstorage\.eu-frankfurt-1\.oraclecloud\.com
OS_URL_PREAUTH=https://your-replacement-url.com
```

### 3. Password Setup

The default password is `password123`. To set a custom password:

1. Generate a SHA256 hash of your password:
   ```python
   import hashlib
   password = "your-new-password"
   hash_value = hashlib.sha256(password.encode()).hexdigest()
   print(hash_value)
   ```

2. Update the `PASSWORD_HASH` in your `.env` file

## Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - Open your browser to `http://localhost:8501`
   - Enter the password to access the chat interface

## Project Structure

```
oci-genai-demo/
├── app.py              # Main application file
├── .env                # Environment variables (create this)
├── requirements.txt    # Python dependencies (create this)
├── README.md          # This file
└── .gitignore         # Git ignore file (recommended)
```

## Creating Requirements File

Create a `requirements.txt` file:

```txt
streamlit>=1.28.0
oci>=2.100.0
python-dotenv>=1.0.0
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OCI_AGENT_ENDPOINT_ID` | ✅ Yes | Your OCI GenAI Agent endpoint ID |
| `OCI_SERVICE_ENDPOINT` | ✅ Yes | OCI GenAI service endpoint URL |
| `PASSWORD_HASH` | ✅ Yes | SHA256 hash of access password |
| `OS_URL` | ✅ Yes | Regex pattern for URL replacement in citations |
| `OS_URL_PREAUTH` | ✅ Yes | Replacement URL for document access |

## Getting Your OCI Agent Endpoint ID

1. Log in to OCI Console
2. Navigate to **AI Services** → **Generative AI Agents**
3. Select your agent
4. Copy the **Agent Endpoint ID** from the details page

## Running the Application

### Local Development
```bash
streamlit run app.py
```

### Production Mode
For production-like local deployment:
```bash
streamlit run app.py --server.port=8501 --server.headless=true
```

### Background Process
To run in background:
```bash
nohup streamlit run app.py > streamlit.log 2>&1 &
```

### Different Port
To run on a different port:
```bash
streamlit run app.py --server.port=8080
```

### Cloud Deployment (Optional)
- **Streamlit Cloud**: Push to GitHub and connect via streamlit.io
- **Direct server deployment**: Copy files to server and run locally

## Customization

### Adding New Preset Questions
Edit the `PRESET_QUESTIONS` list in `app.py`:

```python
PRESET_QUESTIONS = [
    "Your new question here",
    "Another question",
    # ... existing questions
]
```

### Modifying the UI
The app uses standard Streamlit components. Customize by:
- Changing page configuration in `st.set_page_config()`
- Modifying titles and descriptions
- Adding custom CSS with `st.markdown()`

### Citation URL Replacement
Modify `OS_URL` and `OS_URL_PREAUTH` to customize how document URLs are transformed for user access.

## Troubleshooting

### Common Issues

1. **"OCI_AGENT_ENDPOINT_ID environment variable is required"**
   - Check your `.env` file exists and contains the correct endpoint ID

2. **"Failed to initialize OCI client"**
   - Verify your `~/.oci/config` file is correctly configured
   - Ensure your private key file exists and has correct permissions

3. **Authentication errors**
   - Check your OCI credentials and permissions
   - Verify your user has access to the GenAI Agent service

4. **"Password errata. Riprova."**
   - Check your password matches the hash in `PASSWORD_HASH`
   - Default password is `password123`

### Debug Mode
To enable detailed logging, add to your `.env`:
```env
DEBUG_MODE=true
```

## Security Considerations

- Keep your `.env` file secure and never commit it to version control
- Use strong passwords and rotate them regularly
- Ensure your OCI credentials have minimal required permissions
- Consider implementing additional authentication for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues related to:
- **OCI GenAI Agents**: Check OCI documentation and support
- **This application**: Create an issue in the project repository
- **Streamlit**: Visit streamlit.io documentation

---

**Happy coding! 🚀**