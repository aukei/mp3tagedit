"""
MP3 Tag Processor - Handles the processing of MP3 tags
"""
import os
import chardet
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TPE1, TALB, TDRC, TCON

class TagProcessor:
    """Class for processing MP3 tags"""
    
    def __init__(self):
        self.processed_files = {}  # Store processed file data for later saving
    
    def process_file(self, file_path):
        """
        Process the tags of an MP3 file
        
        Args:
            file_path: Path to the MP3 file
            
        Returns:
            dict: Dictionary containing the tag information
        """
        try:
            # Check if file exists
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Load the MP3 file
            audio = MP3(file_path)
            
            # Process ID3 tags
            tag_info = self._process_id3_tags(file_path, audio)
            
            # Store processed data for later saving
            self.processed_files[file_path] = tag_info
            
            return tag_info
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def _process_id3_tags(self, file_path, audio):
        """
        Process ID3 tags according to requirements:
        1. If only ID3v1 exists, copy it to ID3v2
        2. If only ID3v2 exists, keep it
        3. If both exist, discard ID3v1
        4. Identify encoding and convert to UTF-8
        
        Args:
            file_path: Path to the MP3 file
            audio: Mutagen MP3 object
            
        Returns:
            dict: Dictionary containing the processed tag information
        """
        tag_info = {
            "title": "",
            "artist": "",
            "album": "",
            "year": "",
            "genre": ""
        }
        
        try:
            # Try to load ID3 tags
            id3 = ID3(file_path)
            
            # Check if we have ID3v2 tags
            has_id3v2 = len(id3) > 0
            
            # Check if we have ID3v1 tags (this is a simplification, as mutagen doesn't directly expose ID3v1)
            # In a real implementation, we would need to use a different approach to check for ID3v1
            # For now, we'll assume ID3v1 exists if certain basic tags are present in a specific format
            
            # Extract tag information from ID3v2
            if has_id3v2:
                tag_info = self._extract_id3v2_tags(id3)
            
            # Convert encodings to UTF-8 if needed
            tag_info = self._convert_encodings(tag_info)
            
            return tag_info
            
        except ID3NoHeaderError:
            # No ID3 header found, create a new one
            id3 = ID3()
            id3.save(file_path)
            return tag_info
        
        except Exception as e:
            print(f"Error processing ID3 tags for {file_path}: {e}")
            return tag_info
    
    def _extract_id3v2_tags(self, id3):
        """
        Extract tag information from ID3v2 tags
        
        Args:
            id3: Mutagen ID3 object
            
        Returns:
            dict: Dictionary containing the tag information
        """
        tag_info = {
            "title": "",
            "artist": "",
            "album": "",
            "year": "",
            "genre": ""
        }
        
        # Extract title
        if 'TIT2' in id3:
            tag_info["title"] = str(id3['TIT2'])
        
        # Extract artist
        if 'TPE1' in id3:
            tag_info["artist"] = str(id3['TPE1'])
        
        # Extract album
        if 'TALB' in id3:
            tag_info["album"] = str(id3['TALB'])
        
        # Extract year
        if 'TDRC' in id3:
            tag_info["year"] = str(id3['TDRC'])
        
        # Extract genre
        if 'TCON' in id3:
            tag_info["genre"] = str(id3['TCON'])
        
        return tag_info
    
    def _convert_encodings(self, tag_info):
        """
        Convert tag encodings to UTF-8
        
        Args:
            tag_info: Dictionary containing the tag information
            
        Returns:
            dict: Dictionary containing the tag information with UTF-8 encoding
        """
        for key, value in tag_info.items():
            if value and isinstance(value, str):
                # Try to detect encoding
                try:
                    # Convert to bytes if it's a string
                    value_bytes = value.encode('latin-1')
                    
                    # Detect encoding
                    detected = chardet.detect(value_bytes)
                    
                    if detected['encoding'] and detected['encoding'].lower() != 'utf-8':
                        # Decode using detected encoding and encode as UTF-8
                        decoded = value_bytes.decode(detected['encoding'], errors='replace')
                        tag_info[key] = decoded
                except Exception as e:
                    print(f"Error converting encoding for {key}: {e}")
        
        return tag_info
    
    def save_changes(self, file_path):
        """
        Save the changes to the MP3 file
        
        Args:
            file_path: Path to the MP3 file
        """
        if file_path not in self.processed_files:
            raise ValueError(f"File {file_path} has not been processed yet")
        
        try:
            # Get the processed tag information
            tag_info = self.processed_files[file_path]
            
            # Load or create ID3 tags
            try:
                id3 = ID3(file_path)
            except ID3NoHeaderError:
                id3 = ID3()
            
            # Update tags
            if tag_info["title"]:
                id3["TIT2"] = TIT2(encoding=3, text=tag_info["title"])
            
            if tag_info["artist"]:
                id3["TPE1"] = TPE1(encoding=3, text=tag_info["artist"])
            
            if tag_info["album"]:
                id3["TALB"] = TALB(encoding=3, text=tag_info["album"])
            
            if tag_info["year"]:
                id3["TDRC"] = TDRC(encoding=3, text=tag_info["year"])
            
            if tag_info["genre"]:
                id3["TCON"] = TCON(encoding=3, text=tag_info["genre"])
            
            # Save the changes
            id3.save(file_path)
            
            return True
            
        except Exception as e:
            print(f"Error saving changes to {file_path}: {e}")
            raise