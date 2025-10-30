import sys

def main():
    """
    Initialize server and everything
    """
    if len(sys.argv) > 1 and sys.argv[1] == "tui":
        from tui.repl import start_repl
        start_repl()
    else:
        from app import start_server
        start_server()

if __name__ == "__main__":
    main()