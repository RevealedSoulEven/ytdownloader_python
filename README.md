
# YouTube Video Downloader Advanced

This advanced YouTube downloader script, `ytdadvanced.py`, leverages the `yt_dlp` library to download videos, audios, and playlists from YouTube. It offers a flexible approach, allowing users to customize their download preferences either by modifying script parameters directly for a more automated experience or by enabling a CLI mode that prompts for input at runtime.

## Getting Started

### Prerequisites

- Ensure Python is installed on your system.
- The `yt_dlp` library is required. Install it via pip with:

```bash
pip install yt-dlp
```

### Installation

Clone this repository to start using the YouTube Video Downloader Advanced:

```bash
git clone https://github.com/RevealedSoulEven/ytdownloader_python.git
cd your-repository-name
```

## Usage Instructions

### Automated Mode (Edit Script Parameters)

To download content without CLI prompts, edit the `ytdadvanced.py` script directly and set `use_cli` to `False`. Then, adjust the parameters within the script to fit your download needs:

- `video_link`: Set the URL of the YouTube video (ignored if using CLI).
- `download_choice`: Choose between `"audio"` or `"video"`.
- `resolution`: Specify the desired resolution (e.g., 720, 1080). Or you can use any number like 750 and it would download the largest resolution available below 750 like 720p. (or 480p if 720p is not available)
- `use_res`: Set to `True` to use the specified resolution.
- `playlist`: Set to `True` if downloading a playlist.
- `playlist_link`: URL of the playlist to download (required if `playlist` is `True`).
- `concurrent_fragment_downloads`: Number of fragments to download concurrently.
- `download_folder`: Set to `True` to download into a specific folder.
- `downloadfolder`: Name of the folder where downloads will be saved.

After setting your preferences, run the script:

```bash
python ytdadvanced.py
```

### CLI Mode

To use the script in CLI mode, which prompts you for details at runtime, set `use_cli` to `True` in the script. When you run the script, it will ask for all necessary information:

```bash
python ytdadvanced.py
```

This mode allows dynamic input for download links, choice between audio and video, resolution preferences, and more, without needing to edit the script for each download.

## Features

- **Video and Audio Downloads:** Choose to download either the video or just the audio track.
- **Resolution Selection:** Specify your desired resolution for video downloads.
- **Playlist Support:** Download entire playlists by providing the playlist URL.
- **Concurrent Downloads:** Speed up downloads by setting the number of concurrent fragment downloads.
- **Custom Download Folder:** Organize downloads by specifying a folder.

## Contributing

We welcome contributions to improve the script, add new features, or enhance documentation. Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is distributed under the GNU General Public License v3.0, which allows you to copy, modify, and distribute the script as long as changes are open-sourced under the same license.

## Disclaimer

This tool is for personal and educational use only. Please ensure you are authorized to download content from YouTube and adhere to YouTube's Terms of Service.
