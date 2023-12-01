# Convert WAV to MP3

This tool simplifies the process of converting multiple WAV files, both in the current folder and its subfolders, to MP3 format.

- **Source Code:** `1.py`
- **Packaged Executable:** `convert.exe` (located in the `dist` folder)

## How to Use

1. **Download the Executable:**
    Obtain `convert.exe` and place it in a folder containing WAV files.

2. **Install Dependencies:**
    Make sure the required dependencies are installed:
    ```bash
    pip install tqdm ffmpeg-python
    ```

3. **Run the Program:**
    Execute `convert.exe` or use a terminal/command prompt:
    ```Shell
    ./convert.exe
    ```

4. **Conversion Process:**
    - The program scans the current and subfolders for `.wav` files.
    - Converts them to `.mp3`, placing the new files in the same folder.
    - Original `.wav` files are deleted.

5. **Completion:**
    - After completion, the terminal will display "All files converted and deleted."
    - Press Ctrl+C to interrupt if needed.

## Custom Settings

- Customize bitrate and sample_rate during runtime.
    - `bitrate`: Specify MP3 bitrate (default: "320k").
    - `sample_rate`: Specify MP3 sample rate (default: "48000").
    - Example: `./convert.exe --bitrate 192k --sample_rate 44100`
 