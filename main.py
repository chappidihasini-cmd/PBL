"""
main.py
Entry point for MindMapr - Smart Revision Assistant.
Supports both Console-based Menu interface and Desktop GUI mode.
"""

import sys
import os

# Add root folder to sys.path for clean module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.storage import StorageManager
from src.core_operations import RevisionManager
from src.menu_controller import MenuController
from src.output_display import DisplayFormatter


def main() -> None:
    """Initializes and starts the MindMapr application."""
    # Check for CLI arguments
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("MindMapr – Smart Revision Assistant")
        print("\nUsage:")
        print("  python main.py          Launch interactive console menu (default)")
        print("  python main.py --gui    Launch desktop Graphical User Interface (GUI)")
        print("  python gui.py           Directly launch desktop GUI")
        print("  python --help           Show this help message")
        return

    if "--gui" in args or "-g" in args:
        try:
            import gui
            gui.main()
            return
        except ImportError as e:
            DisplayFormatter.print_error(f"Failed to launch GUI: {e}")
            sys.exit(1)

    try:
        storage_manager = StorageManager()
        topics_data = storage_manager.load_data()
        revision_manager = RevisionManager(topics_data)
        menu_controller = MenuController(storage_manager, revision_manager)

        menu_controller.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting MindMapr safely...")
        sys.exit(0)
    except Exception as e:
        DisplayFormatter.print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
