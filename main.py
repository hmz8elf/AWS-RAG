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