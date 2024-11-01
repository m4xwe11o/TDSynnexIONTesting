# TDSynnexIONTesting

This project is designed to interface with the TDSynnex ION API, providing functionality to obtain an access token, list customers, and display results in a user-friendly format. The project setup includes a virtual environment to manage dependencies.

![image](https://github.com/user-attachments/assets/8a17bda0-6602-41ac-8345-8a25f288dbdc)


## Getting Started

Follow these instructions to set up the project on your local machine.

The ION APIv3 documentation can be found here: https://www.tdsynnex.com/ion/v3api/ 

### Prerequisites

1. **Python 3** - Download and install from [python.org](https://www.python.org/).
2. **Git** - Download and install from [git-scm.com](https://git-scm.com/).
3. **GitHub CLI (`gh`)** - Optional, but recommended. Install from [cli.github.com](https://cli.github.com/).

### Project Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/m4xwe11o/TDSynnexIONTesting.git
   cd TDSynnexIONTesting

### Summary of Commands

1. **Clone the repository**: `git clone ...`
2. **Set up virtual environment**: `python3 -m venv venv`
3. **Activate environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Create a `.env`file**: `touch .env`
   
   ```
   # Add the following to .env (edit with your refresh token)
   # .env
   GRANT_TYPE=refresh_token
   REFRESH_TOKEN=  # Replace with your actual refresh token
   ```
6. **Run the app**: `python app.py`


