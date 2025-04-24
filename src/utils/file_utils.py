"""
File utility functions for the MP3 Tag Editor
"""
import os
from pathlib import Path

def get_music_folder():
    """
    Get the user's music folder path
    
    Returns:
        str: Path to the user's music folder
    """
    # Try to get the standard music folder based on the OS
    home = str(Path.home())
    
    # Common music folder locations
    possible_locations = [
        os.path.join(home, "Music"),
        os.path.join(home, "music"),
        os.path.join(home, "Documents", "Music"),
        os.path.join(home, "Documents", "music")
    ]
    
    # Check if any of these locations exist
    for location in possible_locations:
        if os.path.isdir(location):
            return location
    
    # If no music folder is found, return the home directory
    return home

def get_mp3_files(directory, recursive=True):
    """
    Get all MP3 files in a directory
    
    Args:
        directory (str): Directory to search for MP3 files
        recursive (bool): Whether to search recursively
        
    Returns:
        list: List of MP3 file paths
    """
    mp3_files = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.mp3'):
                    mp3_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if file.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(directory, file))
    
    return mp3_files

def get_sample_mp3_files(directory, max_files=10, recursive=True):
    """
    Get a sample of MP3 files from a directory
    
    Args:
        directory (str): Directory to search for MP3 files
        max_files (int): Maximum number of files to return
        recursive (bool): Whether to search recursively
        
    Returns:
        list: List of MP3 file paths
    """
    mp3_files = get_mp3_files(directory, recursive)
    
    # Return a sample of files
    if len(mp3_files) > max_files:
        # Take a distributed sample
        step = len(mp3_files) // max_files
        return mp3_files[::step][:max_files]
    
    return mp3_files