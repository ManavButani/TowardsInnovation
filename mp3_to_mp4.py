from moviepy.editor import *

# Paths to your MP3 and image file
mp3_file = "output_audio.mp3"
image_file = "m.jpg"
output_file = "output_video.mp4"

# Load the audio
audio = AudioFileClip(mp3_file)

# Load the image and set its duration to match the audio's duration
image = ImageClip(image_file).set_duration(audio.duration)

# Set the audio of the image to be the mp3 file
video = image.set_audio(audio)
video.fps = 1
# Export the final video
video.write_videofile(output_file, codec="libx264", audio_codec="aac")
