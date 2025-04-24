#!/usr/bin/env python3
"""
MP3 Tag Editor - A desktop application for mass editing MP3 tags
"""
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("MP3 Tag Editor")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()