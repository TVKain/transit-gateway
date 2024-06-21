from transit.old_api import main as api_main


def main():
    """
    current_path = os.getcwd()

    main_path = os.path.join(current_path, "transit/api/new_main.py")

    command = f"fastapi dev {main_path} --port 2607"

    os.system(command)
    """
    api_main.main()
