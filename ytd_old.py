import yt_dlp
import sys



webm = False

def print_formats_menu(video_info, audio_present, video_present):
    format_list = []

    for i, video_format in enumerate(video_info.get("formats", []), start=1):
        acodec, vcodec = video_format.get("acodec", "none"), video_format.get("vcodec", "none")
        video_ext, audio_ext = video_format.get("video_ext", "none"), video_format.get("audio_ext", "none")
        currext = video_ext if video_ext != "none" else audio_ext
        format_name = video_format.get("format", f"Format {i}")
        isaudio, isvideo = (acodec != "none"), (vcodec != "none")
        if isaudio == audio_present and isvideo == video_present:
            if (currext != "webm" if not webm else currext == "webm"):# and "(" not in format_name:
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
    


url = input("\n\nEnter Video Link: \n")
url = ''.join(url.replace('\n', '').split())
ydlp = yt_dlp.YoutubeDL()
video_info = ydlp.extract_info(url, download=False)

print("\n\n\n\nAvailable Audio + Video formats:\n")
audio_video_formats = print_formats_menu(video_info, True, True)
print("Available Audio Only formats:\n")
audio_formats = print_formats_menu(video_info, True, False)
print("Available Video Only formats:\n")
video_formats = print_formats_menu(video_info, False, True)


format_choices_input = input("Enter the numbers corresponding to formats separated by commas: ")
format_choices = format_choices_input.split(",")

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


if(downloadable):
    download_selected_formats(video_info,format_choices)
