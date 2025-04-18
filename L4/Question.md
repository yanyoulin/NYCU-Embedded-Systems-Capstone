根據你提供的講義《Lect4. speech (2025).1》，以下是我設計的**三題可能會在考試或小考中出現的題目**，**不超出講義內容**，涵蓋：

- 語音處理流程與系統架構  
- 音訊特徵（MFCC、Chroma）  
- Python 語音應用實作（STT/TTS）

---

## 📘 題目一【觀念題】  
**請簡述語音處理系統中「語音識別（Speech Recognition）」的流程與組成模組，並說明 STT 與 TTS 的差別。**

---

### ✅ 解答：

語音處理系統包含以下流程：

1. **使用者發聲** → 麥克風收音（Analog Signal）
2. **Speech Recognition (語音識別 / ASR)**：
   - 將聲音轉為文字（**Speech To Text, STT**）
3. **自然語言處理（NLP）**：
   - 分析語義，理解使用者意圖
4. **產生文字回應**
5. **Text to Speech（TTS）**：
   - 將文字回覆轉為語音播放

---

### STT 與 TTS 差別：

| 名稱 | 全名 | 功能 |
|------|------|------|
| STT | Speech To Text | 將語音轉為文字 |
| TTS | Text To Speech | 將文字轉為語音 |

---

## 📘 題目二【技術題】  
**請說明 MFCC 的完整計算步驟，並說明為何它適合用於語音辨識？**

---

### ✅ 解答：

MFCC（Mel Frequency Cepstral Coefficients）計算步驟：

1. 對每個音訊 Frame 做 **傅立葉轉換（FFT）**
2. 使用 **Mel-Scale 三角形濾波器組** 投影頻譜能量
3. 對每個 mel 頻帶的能量取 **對數**
4. 使用 **離散餘弦轉換（DCT）**，壓縮特徵
5. 得到前 13~20 個 MFCC 係數作為語音特徵向量

---

### MFCC 為何適合語音辨識：

- 模擬人類耳朵對「音高」與「音量」的感知特性
- 可壓縮音訊中的冗餘資訊，保留語意關鍵特徵
- 對雜訊與語者變異具有一定程度的魯棒性

---

## 📘 題目三【程式實作概念題】  
**請說明下列程式碼片段的功能，並指出其輸入與輸出格式：**

```python
from gtts import gTTS
import os

tts = gTTS(text='hello', lang='en')
tts.save('hello.mp3')
os.system('play hello.mp3 > /dev/null 2>&1')
```

---

### ✅ 解答：

這段程式使用 **Google Text-to-Speech (gTTS)** 模組將文字轉為語音：

1. `gTTS(text='hello', lang='en')`  
   → 建立 TTS 物件，輸入文字為 "hello"，語言為英文

2. `tts.save('hello.mp3')`  
   → 將語音存成 MP3 檔案格式

3. `os.system('play hello.mp3 > /dev/null 2>&1')`  
   → 使用系統指令 `play` 播放 MP3 檔案，且將輸出訊息隱藏

---

### 輸入/輸出格式：

| 項目 | 說明 |
|------|------|
| 輸入 | 純文字 `text='hello'` |
| 輸出 | 語音檔案 `hello.mp3`（語音播放） |

---

如果你希望這三題轉為選擇題、填空題，或加入「語音控制 Raspberry Pi 裝置」的應用情境，我可以繼續幫你設計延伸版本。需要嗎？
