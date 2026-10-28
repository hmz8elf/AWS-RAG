"""Entry point of the user-facing interfaces.

Starts the Streamlit WebInterface when the script is run with
`streamlit run main.py`, and the terminal CLIInterface otherwise.
The CLI sends each question to the FastAPI backend (api.py) at EC2_URL.
"""
import sys
from app.interfaces.cliInterface import CLIInterface
from app.interfaces.webInterface import WebInterface

def main() :
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            interface = WebInterface()
        else:
            interface = CLIInterface()
    except Exception:
        interface = CLIInterface()
    interface.start()

if __name__ == "__main__":
    main()