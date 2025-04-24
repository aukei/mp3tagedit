# MP3 Tag Editor

A desktop application for mass editing MP3 tags.

## Features

- Load MP3 files from your music folder
- Process ID3 tags according to the following rules:
  - If only ID3v1 exists, copy it to ID3v2
  - If only ID3v2 exists, keep it
  - If both ID3v1 and ID3v2 exist, discard ID3v1
- Detect and convert tag text encodings to UTF-8
- Preview changes before applying them
- Batch process multiple files at once

## Requirements

- Python 3.8 or higher
- PyQt6
- Mutagen
- Chardet

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mp3tagedit.git
   cd mp3tagedit
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Click "Load MP3 Files" to select MP3 files from your music folder.

3. Click "Process Tags" to analyze and process the tags according to the rules.

4. Review the changes in the table.

5. Click "Save Changes" to apply the changes to the files.

## Development

The application is structured as follows:

- `src/main.py`: Main entry point for the application
- `src/gui/main_window.py`: Main window GUI implementation
- `src/tag_processor/processor.py`: Core tag processing functionality

## License

MIT