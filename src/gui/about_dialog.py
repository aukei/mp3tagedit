"""
About dialog for the MP3 Tag Editor application
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class AboutDialog(QDialog):
    """About dialog for the MP3 Tag Editor application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About MP3 Tag Editor")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("MP3 Tag Editor")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Version
        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Description
        description = """
        <p>A desktop application for mass editing MP3 tags.</p>
        
        <p><b>Features:</b></p>
        <ul>
            <li>Load MP3 files from your music folder</li>
            <li>Process ID3 tags according to specific rules</li>
            <li>Detect and convert tag text encodings to UTF-8</li>
            <li>Preview changes before applying them</li>
            <li>Batch process multiple files at once</li>
        </ul>
        """
        
        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(description_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()