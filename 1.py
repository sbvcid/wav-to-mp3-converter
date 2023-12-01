import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging
import functools
import subprocess
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, input_folder=None, bitrate="320k", sample_rate="48000"):
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

    def has_cuda_support(self):
        try:
            # 嘗試執行帶有 CUDA 支援的 FFmpeg，如果成功返回 True，否則返回 False
            subprocess.run(["ffmpeg", "-hide_banner"], check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def convert_and_delete_wav(self, input_path, output_folder, custom_bitrate):
        try:
            filename, ext = os.path.splitext(os.path.basename(input_path))
            output_folder = os.path.dirname(input_path)  # 使用原始 WAV 文件的相同子文件夾
            output_path = os.path.join(output_folder, f"{filename}.mp3")

            if self.has_cuda_support():
                print("正在使用 CUDA 硬體加速進行轉換.")
                # 使用 subprocess 執行 FFmpeg 命令，啟用 CUDA 硬體加速
                cmd = [
                    "ffmpeg",
                    "-hwaccel", "cuda",
                    "-i", rf"{input_path}",
                    "-c:a", "libmp3lame",
                    "-b:a", custom_bitrate,
                    rf"{output_path}"
                ]
            else:
                print("未檢測到 CUDA 硬體加速支援，將使用軟體編碼器進行轉換.")
                # 回落到軟體編碼器
                cmd = [
                    "ffmpeg",
                    "-i", rf"{input_path}",
                    "-c:a", "libmp3lame",
                    "-b:a", custom_bitrate,
                    rf"{output_path}"
                ]

            # 指定 stdout 和 stderr 的編碼為 "utf-8"
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")

            # 將 stdout 和 stderr 的內容打印出來
            print(result.stdout)
            print(result.stderr)

            os.remove(input_path)

            return f"轉換 {filename} 完成，並刪除原始 WAV 檔案"
        except FileNotFoundError:
            logging.warning(f"文件 {input_path} 未找到")
        except PermissionError as e:
            logging.error(f"PermissionError: {e}")

def process_files(bitrate="320k", sample_rate="48000"):
    current_folder = os.path.abspath(".")
    output_folder = current_folder  # 使用原始資料夾的路徑

    audio_processor = AudioProcessor(bitrate=bitrate, sample_rate=sample_rate)
    wav_files = audio_processor.find_wav_files()
    total_files = len(wav_files)

    print(f"Found {total_files} WAV files to process with bitrate={bitrate} and sample_rate={sample_rate}.")

    progress = 0

    with ThreadPoolExecutor(max_workers=8) as executor, tqdm(total=total_files) as pbar:
        try:
            # 使用 functools.partial 建立包裝器函數，固定前三個參數
            wrapper = functools.partial(audio_processor.convert_and_delete_wav, output_folder=output_folder, custom_bitrate=bitrate)
            for result in executor.map(wrapper, wav_files):
                progress += 1
                pbar.update(1)
                pbar.set_description(f"處理進度：{progress}/{total_files} ({(progress / total_files) * 100:.2f}%) - {result}")
        except KeyboardInterrupt:
            print("User interrupted the process.")

    print("\n所有檔案轉換和刪除完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="將WAV轉換成MP3")
    parser.add_argument("--bitrate", default="320k", help="MP3 bitrate, e.g., '192k'")
    parser.add_argument("--sample_rate", default="48000", help="Sample rate, e.g., '44100'")
    args = parser.parse_args()

    process_files(bitrate=args.bitrate, sample_rate=args.sample_rate)
    print("Press Enter to exit...")
    input()
