import yt_dlp
import sys




"""
DEPRECATED: This script is no longer recommended for use and may not function as intended.
Please use `ytdadvanced.py` for an updated and more feature-rich YouTube downloading experience.
"""



"""
DEPRECATED: This script is no longer recommended for use and may not function as intended.
Please use `ytdadvanced.py` for an updated and more feature-rich YouTube downloading experience.
"""



"""
DEPRECATED: This script is no longer recommended for use and may not function as intended.
Please use `ytdadvanced.py` for an updated and more feature-rich YouTube downloading experience.
"""





arguments = sys.argv
webm = False if len(arguments) == 1 else True
def print_formats_menu(video_info, audio_present, video_present):
    format_list = []

    for i, video_format in enumerate(video_info.get("formats", []), start=1):
        acodec, vcodec = video_format.get("acodec", "none"), video_format.get("vcodec", "none")
        video_ext, audio_ext = video_format.get("video_ext", "none"), video_format.get("audio_ext", "none")
        currext = video_ext if video_ext != "none" else audio_ext
        format_name = video_format.get("format", f"Format {i}")
        isaudio, isvideo = (acodec != "none"), (vcodec != "none")
        if isaudio == audio_present and isvideo == video_present:
            if currext != "webm" if not webm else currext == "webm":
                format_list.append(i)
                tempuu = str(i)+"."
                print(f"{tempuu: <3}  {format_name: <28}   {currext}")

    print("\n\n")
    return format_list


def download_selected_formats(video_info, formats):
    options = {}
    title = video_info.get("title", "video")
    output_filen = title.replace(' ', '_')
    output_filename = ''.join(char for char in output_filen if char.isalnum() or char in '~[]!@#$%^&*()_+/., ')
    max_filename_length = 120 #max 127 by android
    output_filename = output_filename[:max_filename_length]
    
    
    if len(formats) == 1:
        curr_format = video_info.get("formats", [])[int(formats[0]) - 1]
        output_filename += f".{curr_format['ext']}"
        options = {
            'format': f"{curr_format['format_id']}",
            'outtmpl': output_filename,
            'concurrent_fragment_downloads': 20
        }
            
    if len(formats) == 2:
        audio_choice, video_choice = map(int, format_choices)
        curr_format = video_info.get("formats", [])[video_choice - 1]
        curr_format_audio = video_info.get("formats", [])[audio_choice - 1]
        output_filename += f".{curr_format['ext']}"
        
        options = {
            'format': f"{curr_format['format_id']}+{curr_format_audio['format_id']}",
            'outtmpl': output_filename,
            'concurrent_fragment_downloads': 20
        }
        
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(video_info.get("original_url",""))

if __name__ == "__main__":
    video_urls_input = input("\nEnter multiple video links separated by commas: ")
    video_urls = video_urls_input.split(",")

    all_video_info = []
    all_quality_options = []

    for url in video_urls:
        ydlp = yt_dlp.YoutubeDL()
        video_info = ydlp.extract_info(url, download=False)
        all_video_info.append((url, video_info))

    for url, video_info in all_video_info:
        vid_title = video_info.get("title","") if video_info.get("title","") != "" else url
        print(f"\n\n\n\nVideo :: {vid_title}\n\n")
        print("Available Audio + Video formats:\n")
        audio_video_formats = print_formats_menu(video_info, True, True)
        print("Available Audio Only formats:\n")
        audio_formats = print_formats_menu(video_info, True, False)
        print("Available Video Only formats:\n")
        video_formats = print_formats_menu(video_info, False, True)
        format_choices_input = input("Enter the numbers corresponding to formats separated by commas: ")

        quality_options = {"url": url, "choices": format_choices_input, "audvid": audio_video_formats, "aud": audio_formats, "vid": video_formats}
        all_quality_options.append(quality_options)

    for quality_options in all_quality_options:
        url = quality_options["url"]
        format_choice = quality_options["choices"]
        audio_video_formats = quality_options["audvid"]
        audio_formats = quality_options["aud"]
        video_formats = quality_options["vid"]
        format_choices = format_choice.split(",")
        downloadable = True
        if len(format_choices) == 1:
            choice = int(format_choices[0])
            if choice in audio_video_formats:
                print("User selected format: Audio + Video")
            elif choice in audio_formats:
                print("User selected format: Audio Only")
            elif choice in video_formats:
                print("User selected format: Video Only")
            else:
                downloadable = False
                print("Invalid format choice. Please enter a valid format number.")
        elif len(format_choices) == 2:
            audio_choice, video_choice = map(int, format_choices)
            if audio_choice in audio_formats and video_choice in video_formats:
                print("User selected formats: Audio and Video separately")
            else:
                downloadable = False
                print("Invalid format choices. Please enter valid format numbers.")
        else:
            downloadable = False
            print("Invalid number of format choices. Please enter either 1 or 2 format numbers.")

        if not downloadable:
            print(f"Skipping download for video '{all_video_info[video_urls.index(url)][1].get('title')}' due to invalid format choice.")
            continue

        download_selected_formats(all_video_info[video_urls.index(url)][1], format_choices)

    print("All videos downloaded successfully.")
