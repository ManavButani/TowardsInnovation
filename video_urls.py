from pytube import Playlist

# Enter your YouTube playlist URL here
playlist_url = "https://youtube.com/playlist?list=PLxNHpNhDaEFLTT826yucpRLr6TAMSKziU&si=bV1zJRY7nPANGm79"

# Create Playlist object
playlist = Playlist(playlist_url)

output_file = "playlist_video_urls.txt"

with open(output_file, "w") as file:
    for index, video_url in enumerate(playlist.video_urls):
        print(index)
        file.write(f"'{video_url}'" + "\n")