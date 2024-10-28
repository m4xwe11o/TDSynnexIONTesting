# TDSynnexIONTesting

This project is designed to interface with the TDSynnex ION API, providing functionality to obtain an access token, list customers, and display results in a user-friendly format. The project setup includes a virtual environment to manage dependencies.

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

1. **Python 3** - Download and install from [python.org](https://www.python.org/).
2. **Git** - Download and install from [git-scm.com](https://git-scm.com/).
3. **GitHub CLI (`gh`)** - Optional, but recommended. Install from [cli.github.com](https://cli.github.com/).

### Project Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/TDSynnexIONTesting.git
   cd TDSynnexIONTesting

### Summary of Commands

1. **Clone the repository**: `git clone ...`
2. **Set up virtual environment**: `python3 -m venv venv`
3. **Activate environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Create a `.env`file**: `touch .env`
   
   ```
   # Add the following to .env (edit with your refresh token)
   ACCESS_TOKEN=
   REFRESH_TOKEN=your-refresh-token
   ```
6. **Run the app**: `python app.py`

