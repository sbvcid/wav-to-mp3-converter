import os
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from tqdm import tqdm
import logging
import sys
import functools  # 加入這一行

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, input_folder=None, bitrate="192k", sample_rate="44100"):
        self.input_folder = input_folder or os.path.abspath(".")
        self.bitrate = bitrate
        self.sample_rate = sample_rate

    def find_wav_files(self):
        wav_files = []
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                if file.endswith(".wav"):
                    wav_files.append(os.path.join(root, file))
        return wav_files

    def convert_and_delete_wav(self, input_path, output_folder):
        try:
            filename, ext = os.path.splitext(os.path.basename(input_path))
            output_path = os.path.join(output_folder, f"{filename}.mp3")

            audio = AudioSegment.from_wav(input_path)
            audio.export(output_path, format="mp3", bitrate=self.bitrate, parameters=["-ar", self.sample_rate])

            os.remove(input_path)

            return f"轉換 {filename} 完成，並刪除原始 WAV 檔案"
        except FileNotFoundError:
            logging.warning(f"文件 {input_path} 未找到")
        except PermissionError as e:
            logging.error(f"PermissionError: {e}")

def process_files(bitrate="192k", sample_rate="44100"):
    current_folder = os.path.abspath(".")
    output_folder = current_folder  # 使用原始資料夾的路徑

    audio_processor = AudioProcessor()
    wav_files = audio_processor.find_wav_files()
    total_files = len(wav_files)

    print(f"Found {total_files} WAV files to process.")

    progress = 0

    with ThreadPoolExecutor(max_workers=8) as executor, tqdm(total=total_files) as pbar:
        try:
            # 使用 functools.partial 建立包裝器函數，固定前兩個參數
            wrapper = functools.partial(audio_processor.convert_and_delete_wav, output_folder=output_folder)
            for result in executor.map(wrapper, wav_files):
                progress += 1
                pbar.update(1)
                pbar.set_description(f"處理進度：{progress}/{total_files} ({(progress / total_files) * 100:.2f}%) - {result}")
        except KeyboardInterrupt:
            print("User interrupted the process.")

    print("\n所有檔案轉換和刪除完成")

if __name__ == "__main__":
    process_files()
    print("Press Enter to exit...")
    input()
