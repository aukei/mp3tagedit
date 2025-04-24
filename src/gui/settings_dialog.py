"""
Settings dialog for the MP3 Tag Editor application
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QCheckBox, QSpinBox, QFormLayout)
from PyQt6.QtCore import Qt
from utils.config import load_config, save_config

class SettingsDialog(QDialog):
    """Settings dialog for the MP3 Tag Editor application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        
        self.config = load_config()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Form layout for settings
        form_layout = QFormLayout()
        
        # Sample size
        self.sample_size_spin = QSpinBox()
        self.sample_size_spin.setMinimum(1)
        self.sample_size_spin.setMaximum(100)
        self.sample_size_spin.setValue(self.config.get("sample_size", 10))
        form_layout.addRow("Sample size:", self.sample_size_spin)
        
        # Recursive search
        self.recursive_checkbox = QCheckBox()
        self.recursive_checkbox.setChecked(self.config.get("recursive_search", True))
        form_layout.addRow("Search recursively:", self.recursive_checkbox)
        
        # Auto process
        self.auto_process_checkbox = QCheckBox()
        self.auto_process_checkbox.setChecked(self.config.get("auto_process", False))
        form_layout.addRow("Auto-process files after loading:", self.auto_process_checkbox)
        
        layout.addLayout(form_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def save_settings(self):
        """Save the settings"""
        self.config["sample_size"] = self.sample_size_spin.value()
        self.config["recursive_search"] = self.recursive_checkbox.isChecked()
        self.config["auto_process"] = self.auto_process_checkbox.isChecked()
        
        save_config(self.config)
        self.accept()