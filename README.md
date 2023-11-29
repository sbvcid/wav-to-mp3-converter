# 我的項目

這個項目用來將當前資料夾中的WAV檔案轉換成MP3檔案
1.py是原始代碼，在dist中的1.exe是打包後的執行檔

## 如何使用

1. 下載項目的執行檔（`1.exe`），放入有WAV檔案的資料夾中。
2. 點擊執行
    或者開啟終端機或命令提示字元。運行以下命令啟動程式：
    ```sh
    ./1.exe
    ```
3. 程式將遍歷當前資料夾中，以及子資料夾的 `.wav` 檔案，將它們轉換成 `.mp3` 檔案，並刪除原始的 `.wav` 檔案。
4. 程式運行完成後，終端機會顯示 "所有檔案轉換和刪除完成"。

## 代碼示例

以下是程式的基本結構：

```python

from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from tqdm import tqdm
import logging
import os
import functools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, input_folder=None, bitrate="192k", sample_rate="44100"):
        self.input_folder = input_folder or os.path.dirname(os.path.abspath(__file__))
        self.bitrate = bitrate
        self.sample_rate = sample_rate

    def find_wav_files(self):
        wav_files = []
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                if file.endswith(".wav"):
                    wav_files.append(os.path.abspath(os.path.join(root, file)))
        return wav_files

    def convert_and_delete_wav(self, input_path):
        try:
            filename, ext = os.path.splitext(os.path.basename(input_path))
            output_path = os.path.join(os.path.dirname(input_path), f"{filename}.mp3")

            audio = AudioSegment.from_wav(input_path)
            audio.export(output_path, format="mp3", bitrate=self.bitrate, parameters=["-ar", self.sample_rate])

            os.remove(input_path)

            return f"轉換 {filename} 完成，並刪除原始 WAV 檔案"
        except FileNotFoundError:
            logging.warning(f"文件 {input_path} 未找到")
        except PermissionError as e:
            logging.error(f"PermissionError: {e}")

def process_files(bitrate="192k", sample_rate="44100"):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = current_folder  # 使用原始資料夾的路徑

    audio_processor = AudioProcessor()  # 创建 AudioProcessor 实例
    wav_files = audio_processor.find_wav_files()  # 调用 find_wav_files 方法
    total_files = len(wav_files)

    print(f"Found {total_files} WAV files to process.")

    progress = 0

    with ThreadPoolExecutor(max_workers=8) as executor, tqdm(total=total_files) as pbar:
        try:
            # 使用 functools.partial 建立包裝器函數，固定前兩個參數
    
