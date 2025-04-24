"""
Main window for the MP3 Tag Editor application
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QFileDialog, QMessageBox, QLabel, QHeaderView,
                            QCheckBox, QSpinBox, QProgressBar, QMenuBar, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from tag_processor.processor import TagProcessor
from utils.file_utils import get_music_folder, get_sample_mp3_files
from gui.about_dialog import AboutDialog

class MainWindow(QMainWindow):
    """Main window for the MP3 Tag Editor application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP3 Tag Editor")
        self.setMinimumSize(800, 600)
        
        self.tag_processor = TagProcessor()
        self.mp3_files = []
        self.processed_data = {}  # Store processed data for each file
        
        self.init_ui()
        self.create_menu_bar()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Add buttons
        self.load_button = QPushButton("Load MP3 Files")
        self.load_button.clicked.connect(self.load_mp3_files)
        button_layout.addWidget(self.load_button)
        
        self.sample_button = QPushButton("Sample MP3 Files")
        self.sample_button.clicked.connect(self.sample_mp3_files)
        button_layout.addWidget(self.sample_button)
        
        self.process_button = QPushButton("Process Tags")
        self.process_button.clicked.connect(self.process_tags)
        self.process_button.setEnabled(False)
        button_layout.addWidget(self.process_button)
        
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
        
        # Sample options layout
        sample_options_layout = QHBoxLayout()
        
        # Add sample options
        sample_options_layout.addWidget(QLabel("Sample size:"))
        
        self.sample_size_spin = QSpinBox()
        self.sample_size_spin.setMinimum(1)
        self.sample_size_spin.setMaximum(100)
        self.sample_size_spin.setValue(10)
        sample_options_layout.addWidget(self.sample_size_spin)
        
        self.recursive_checkbox = QCheckBox("Search recursively")
        self.recursive_checkbox.setChecked(True)
        sample_options_layout.addWidget(self.recursive_checkbox)
        
        sample_options_layout.addStretch()
        
        main_layout.addLayout(sample_options_layout)
        
        # Status label
        self.status_label = QLabel("Ready. Click 'Load MP3 Files' to start or 'Sample MP3 Files' to get samples from your music folder.")
        main_layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Table for displaying MP3 files and their tags
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(6)
        self.files_table.setHorizontalHeaderLabels(["Filename", "Title", "Artist", "Album", "Year", "Genre"])
        self.files_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        # Make cells editable except for the filename column
        self.files_table.itemChanged.connect(self.on_table_item_changed)
        
        main_layout.addWidget(self.files_table)
        
        self.setCentralWidget(main_widget)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Load action
        load_action = QAction("&Load MP3 Files", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_mp3_files)
        file_menu.addAction(load_action)
        
        # Sample action
        sample_action = QAction("&Sample MP3 Files", self)
        sample_action.setShortcut("Ctrl+S")
        sample_action.triggered.connect(self.sample_mp3_files)
        file_menu.addAction(sample_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        
        # Process action
        process_action = QAction("&Process Tags", self)
        process_action.setShortcut("Ctrl+P")
        process_action.triggered.connect(self.process_tags)
        edit_menu.addAction(process_action)
        
        # Save action
        save_action = QAction("&Save Changes", self)
        save_action.setShortcut("Ctrl+Shift+S")
        save_action.triggered.connect(self.save_changes)
        edit_menu.addAction(save_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def show_about_dialog(self):
        """Show the about dialog"""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def load_mp3_files(self):
        """Load MP3 files from the user's music folder"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("MP3 files (*.mp3)")
        
        # Start in the music folder
        file_dialog.setDirectory(get_music_folder())
        
        if file_dialog.exec():
            self.mp3_files = file_dialog.selectedFiles()
            self.status_label.setText(f"Loaded {len(self.mp3_files)} MP3 files.")
            self.process_button.setEnabled(True)
            self.display_files()
    
    def sample_mp3_files(self):
        """Sample MP3 files from the user's music folder"""
        music_folder = get_music_folder()
        
        if not music_folder:
            QMessageBox.warning(
                self,
                "Music Folder Not Found",
                "Could not find your music folder. Please use 'Load MP3 Files' to select files manually."
            )
            return
        
        # Get sample size and recursive option
        sample_size = self.sample_size_spin.value()
        recursive = self.recursive_checkbox.isChecked()
        
        # Get sample MP3 files
        self.mp3_files = get_sample_mp3_files(music_folder, sample_size, recursive)
        
        if not self.mp3_files:
            QMessageBox.warning(
                self,
                "No MP3 Files Found",
                f"No MP3 files found in {music_folder}. Please use 'Load MP3 Files' to select files manually."
            )
            return
        
        self.status_label.setText(f"Sampled {len(self.mp3_files)} MP3 files from {music_folder}.")
        self.process_button.setEnabled(True)
        self.display_files()
    
    def display_files(self):
        """Display the loaded MP3 files in the table"""
        # Disconnect the itemChanged signal to prevent triggering while populating
        self.files_table.itemChanged.disconnect(self.on_table_item_changed)
        
        self.files_table.setRowCount(len(self.mp3_files))
        
        for row, file_path in enumerate(self.mp3_files):
            # Display filename
            filename = file_path.split("/")[-1]
            filename_item = QTableWidgetItem(filename)
            filename_item.setFlags(filename_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make filename non-editable
            self.files_table.setItem(row, 0, filename_item)
            
            # Other columns will be filled after processing
            for col in range(1, 6):
                self.files_table.setItem(row, col, QTableWidgetItem(""))
        
        # Reconnect the itemChanged signal
        self.files_table.itemChanged.connect(self.on_table_item_changed)
    
    def process_tags(self):
        """Process the tags of the loaded MP3 files"""
        if not self.mp3_files:
            return
        
        self.status_label.setText("Processing tags...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(self.mp3_files))
        self.progress_bar.setValue(0)
        
        # Disconnect the itemChanged signal to prevent triggering while populating
        self.files_table.itemChanged.disconnect(self.on_table_item_changed)
        
        # Process each file
        for row, file_path in enumerate(self.mp3_files):
            try:
                tag_info = self.tag_processor.process_file(file_path)
                
                # Store processed data
                self.processed_data[file_path] = tag_info
                
                # Update table with tag information
                if tag_info:
                    self.files_table.setItem(row, 1, QTableWidgetItem(tag_info.get("title", "")))
                    self.files_table.setItem(row, 2, QTableWidgetItem(tag_info.get("artist", "")))
                    self.files_table.setItem(row, 3, QTableWidgetItem(tag_info.get("album", "")))
                    self.files_table.setItem(row, 4, QTableWidgetItem(str(tag_info.get("year", ""))))
                    self.files_table.setItem(row, 5, QTableWidgetItem(tag_info.get("genre", "")))
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
            
            self.progress_bar.setValue(row + 1)
        
        # Reconnect the itemChanged signal
        self.files_table.itemChanged.connect(self.on_table_item_changed)
        
        self.status_label.setText(f"Processed {len(self.mp3_files)} files. You can edit tags directly in the table. Click 'Save Changes' to apply.")
        self.save_button.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def on_table_item_changed(self, item):
        """Handle changes to table items"""
        row = item.row()
        col = item.column()
        
        if col == 0 or row >= len(self.mp3_files):
            return  # Ignore changes to filename column or invalid rows
        
        file_path = self.mp3_files[row]
        
        if file_path not in self.processed_data:
            return
        
        # Update the processed data with the new value
        tag_keys = ["title", "artist", "album", "year", "genre"]
        tag_key = tag_keys[col - 1]  # Adjust for filename column
        
        self.processed_data[file_path][tag_key] = item.text()
        
        # Update the tag processor's data
        self.tag_processor.processed_files[file_path] = self.processed_data[file_path]
    
    def save_changes(self):
        """Save the changes to the MP3 files"""
        reply = QMessageBox.question(
            self, 
            "Confirm Changes",
            f"Are you sure you want to save changes to {len(self.mp3_files)} files?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.status_label.setText("Saving changes...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, len(self.mp3_files))
            self.progress_bar.setValue(0)
            
            success_count = 0
            for i, file_path in enumerate(self.mp3_files):
                try:
                    self.tag_processor.save_changes(file_path)
                    success_count += 1
                except Exception as e:
                    print(f"Error saving changes to {file_path}: {e}")
                
                self.progress_bar.setValue(i + 1)
            
            self.status_label.setText(f"Successfully saved changes to {success_count} files.")
            self.progress_bar.setVisible(False)
            
            # Reset buttons
            self.save_button.setEnabled(False)
            self.process_button.setEnabled(False)
            self.mp3_files = []
            self.processed_data = {}