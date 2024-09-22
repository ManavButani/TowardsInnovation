import yt_dlp

ydl_opts ={}
ydl_opts = {
    'format': 'bestvideo[height<=720]+bestaudio',  # 720p video
    # 'outtmpl': '%(title)s.%(ext)s',  # Set output filename format
    'output_format': 'mp4',    # Ensure video and audio are merged into MP4
    # 'postprocessors': [{
    #     'key': 'FFmpegVideoConvertor',
    #     'preferedformat': 'mp4'      # Convert to mp4 after downloading
    # }]
}

def dwl_vid(video_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

channel = 1
while channel == 1:
    # link_of_the_video = input("Copy & paste the URL of the YouTube video you want to download: ")
    # zxt = link_of_the_video.strip()
    downloaded = []
    for url in [
# 'https://www.youtube.com/watch?v=H7s0dYHC0_c'
# 'https://www.youtube.com/watch?v=yoRllwA1P0Y'
# 'https://www.youtube.com/watch?v=MYa67CegX18'
# 'https://www.youtube.com/watch?v=ZzVmGg4AaL4',
# 'https://www.youtube.com/watch?v=QSibwmqv9I8',
# 'https://www.youtube.com/watch?v=6XeoyLGMmGQ',
# 'https://www.youtube.com/watch?v=GjRK385t2XI',
# 'https://www.youtube.com/watch?v=Z9zwUzMcbEg',
# 'https://www.youtube.com/watch?v=Dq7qSaVjZR4',
# 'https://www.youtube.com/watch?v=rzAPFYrVvyQ',
# 'https://www.youtube.com/watch?v=VjA1c6GlU1M',
# 'https://www.youtube.com/watch?v=jZQskY4O4xk',
# 'https://www.youtube.com/watch?v=7Lfi7rfRjr0',
# 'https://www.youtube.com/watch?v=98efa_DisZ0',
# 'https://www.youtube.com/watch?v=aHMbXaLBD9Q',
# 'https://www.youtube.com/watch?v=KbE2J2qWWcs',
# 'https://www.youtube.com/watch?v=v4b--kcS_iw',
]:
        if url not in downloaded:
            dwl_vid(url.strip())
            downloaded.append(url)
    # channel = int(input("Enter 1 if you want to download more videos\nEnter 0 if you are done: "))


