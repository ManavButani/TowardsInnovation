import yt_dlp

ydl_opts = {
    'format': 'bestvideo[height<=720]+bestaudio',  # 720p video
    # 'outtmpl': '%(title)s.%(ext)s',  # Set output filename format
    # 'merge_output_format': 'mp4',    # Ensure video and audio are merged into MP4
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
    for url in [
# 'https://youtu.be/jvNFWJCNLSg?si=dKEU-K94w01LHTVF',
# 'https://youtu.be/R-gmTmrJJ1g?si=s2CLJFzXnyZybwbU',
# 'https://youtu.be/QVV6D-wwAMQ?si=r1vFxQjyhm1DP7Ov',
# 'https://youtu.be/wKvjbay_CW0?si=ZbA0UYr0RHK7eI76',
# 'https://youtu.be/yj6Rulvi4yo?si=SJT8dSf4iCfQX9dn',
# 'https://youtu.be/biZSPM0XJAM?si=G_e90pQo8HFtVdIu',
# 'https://youtu.be/g4N_ijMbhuE?si=ZcE38wxyXm20CVD0',
# 'https://youtu.be/ykPZi511fDc?si=PEsO_pw1qLHxR5Wk',
# 'https://youtu.be/R7hL5YNGA8c?si=B47UZvj4Ie8omt3U',
# 'https://youtu.be/tfIIBLUSnWc?si=wuV3kIE0cnMx0qlv',
'https://youtu.be/j2irsMtBshQ?si=gK7BPfpn6rm9LM6F',
'break'
]:
        if url=='break':
            exit()
        dwl_vid(url.strip())
    # channel = int(input("Enter 1 if you want to download more videos\nEnter 0 if you are done: "))


