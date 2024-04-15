import os

def delete_audio_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(script_dir, "audio")  # Relative path to the audio folder
    
    # Iterate over the files in the audio folder
    for filename in os.listdir(audio_folder):
        file_path = os.path.join(audio_folder, filename)
        
        # Check if the file exists and is a file (not a directory)
        if os.path.isfile(file_path):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {file_path}")
                print(f"Error message: {str(e)}")
    
    print("Audio files deletion completed.")
