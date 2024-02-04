import yt_dlp




# Configuration options
use_cli = False
video_link = "https://www.youtube.com/watch?v=NbyHNASFi6U" # only for non-cli
download_choice = "video" # audio or video
resolution = 720
use_res = True
playlist = True
playlist_link = "https://www.youtube.com/playlist?list=PL9bw4S5ePsEGx_-Jpy_xrC6JqIRCNYDZ9"
concurrent_fragment_downloads = 30
download_folder = True
downloadfolder = "ytdown"





"""
Copyright (c) 2024 RevealedSoulEven

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""














def find_corresponding_element(list1, list2, r): #to get corresponding resolution available
    max_value = -1
    corresponding_element = None
    for index, value in enumerate(list2):
        if value <= r and value > max_value:
            max_value = value
            corresponding_element = list1[index]
    return corresponding_element
    


def get_best_audio(video_info):
    audio_format = 0
    for i, video_format in enumerate(video_info.get("formats", []), start=1):
        acodec, vcodec = video_format.get("acodec", "none"), video_format.get("vcodec", "none")
        audio_ext = video_format.get("audio_ext", "none")
        format_id = video_format.get("format_id", f"Format {i}")
        isaudio, isvideo = (acodec != "none"), (vcodec != "none")
        # get video
        if isaudio == True and isvideo == False:
            if audio_ext == "m4a":
                audio_format = format_id
    #######
    title = video_info.get("title", "video")
    output_filen = title.replace(' ', '_')
    output_filename = ''.join(char for char in output_filen if char.isalnum() or char in '~[]!@#$%^&*()_+/., ')
    max_filename_length = 120 #max 127 by android
    output_filename = output_filename[:max_filename_length]
    return [audio_format, output_filename]


def download_audio(video_info):
    dataa = get_best_audio(video_info)
    options = {
        'quiet': True,
        'format': f'{dataa[0]}',
        'outtmpl': f'{downloadfolder}{dataa[1]}.m4a',
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])


def download_video(video_info):
    if not use_res:
        print("\nAvailable Video Formats:")
    format_list = []
    format_height = []
    ######
    for i, video_format in enumerate(video_info.get("formats", []), start=1):
        acodec, vcodec = video_format.get("acodec", "none"), video_format.get("vcodec", "none")
        video_ext, audio_ext = video_format.get("video_ext", "none"), video_format.get("audio_ext", "none")
        currext = video_ext if video_ext != "none" else audio_ext
        format_name = video_format.get("format", f"Format {i}")
        format_id = video_format.get("format_id", f"Format {i}")
        format_h = video_format.get("height", f"Format {i}")
        isaudio, isvideo = (acodec != "none"), (vcodec != "none")
        # get video
        if isaudio == False and isvideo == True:
            if currext != "webm" and "(" not in format_name and "m3u8" in video_format.get("protocol","") and len(vcodec) < 15:
                if format_h in format_height:
                    index = format_height.index(format_h)
                    format_height.pop(index)
                    format_list.pop(index)
                format_list.append(int(format_id))
                format_height.append(format_h)
                tempuu = str(i)+"."
                if not use_res:
                    print(f"{tempuu: <3}  {format_name: <28}   {currext}")
    #####
    if use_res == False:
        format_id = input("Enter format_id for video: ").strip()
    else:
        format_id = find_corresponding_element(format_list, format_height, resolution)
    dataa = get_best_audio(video_info)
    options = {
        'quiet': True,
        'format': f'{format_id}+{dataa[0]}',
        'outtmpl': f'{downloadfolder}{dataa[1]}.mp4',
        'concurrent_fragment_downloads': concurrent_fragment_downloads
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])




if download_folder:
    downloadfolder += "/"
else:
    downloadfolder = ""

if use_cli:
    if playlist:
        playlist_link = input("Enter Playlist Link: ").strip()
    else:
        video_link = input("Enter Video Link: ").strip()
    download_choice = input("Download (a/v): ").lower().strip()
    if download_choice == "a" or download_choice == "v":
        download_choice = "audio" if download_choice == "a" else "video"
    else:
        print("Please Enter a valid Choice")
        
playlist_videos = []
has_vids_in_playlist = False
if playlist:
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_link, download=False)
        if 'entries' in result:
            for video in result['entries']:
                if 'url' in video:
                    playlist_videos.append(video["url"])
                    has_vids_in_playlist = True
            if has_vids_in_playlist:
                print("Total ",len(playlist_videos)," videos found in Playlist")
        else:
            print("No Videos Found in Playlist")


ydl_opts = {'quiet': True}
playlist_vid_info = []
if playlist and has_vids_in_playlist:
    progress = 0
    for vids in playlist_videos:
        progress += 1
        print("extracting ",progress)
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_vid_info.append(ydl.extract_info(vids, download=False))
        except:
            pass
elif not playlist:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_link, download=False)






if download_choice == 'video':
    if playlist and has_vids_in_playlist:
        if not use_res:
            resolution = int(input("Enter resolution: "))
            use_res = True
        for vidss in playlist_vid_info:
            download_video(vidss)
    elif not playlist:
        download_video(video_info)
else:
    if playlist and has_vids_in_playlist:
        for vidss in playlist_vid_info:
            download_audio(vidss)
    elif not playlist:
        download_audio(video_info)
