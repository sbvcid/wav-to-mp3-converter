# 把 WAV 轉換成 MP3 (Convert WAV to MP3)

這個小工具可以幫助你將當前資料夾中，以及子資料夾的所有 WAV 檔案批量轉換為 MP3 格式。

`1.py` 是原始碼，`dist` 中的 `convert.exe` 是打包後的執行檔。

## 如何使用

1. 下載執行檔（`convert.exe`），放入有 WAV 檔案的資料夾中。
2. **安裝依賴庫 ffmpeg-python：**
    請確保你已經安裝了必要的依賴庫，你可以使用以下指令進行安裝：
   ```bash
   pip install tqdm ffmpeg-python
3. 點擊執行檔（convert.exe）執行程式，或者開啟終端機或命令提示字元。運行以下命令啟動程式：./convert.exe
4. 等待轉換：程式將遍歷當前資料夾中，以及子資料夾的 .wav 檔案，將它們轉換成 .mp3 檔案，放在在相同的資料夾中，並刪除原始的 .wav 檔案。
5. 程式運行完成後，終端機會顯示 "所有檔案轉換和刪除完成"。若中途想停止，按下Ctrl+C可以中斷。


## 自定義設定

您可以在執行時通過命令行參數自定義 bitrate、sample_rate。例如：./convert.exe --bitrate 192k --sample_rate 44100 

bitrate：指定 MP3 的位元率，預設為 "320k"。
sample_rate：指定 MP3 的取樣率，預設為 "48000"。


