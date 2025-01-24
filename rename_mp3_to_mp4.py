import os

# Specify the directory containing the .webm files
directory = "./"  # Use "." for the current directory, or replace with a specific path

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".webm"):
        # Generate the new filename with .mp3 extension
        new_filename = os.path.splitext(filename)[0] + ".mp3"
        
        # Rename the file
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")

print("All .webm files have been renamed to .mp3!")
