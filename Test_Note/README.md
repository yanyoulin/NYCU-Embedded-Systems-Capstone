# NYCU-Embedded-Systems-Capstone
這裡是根據你目前上傳的程式檔案所設計的**Debug 題型（含解答）**，涵蓋常見錯誤類型（如語法錯誤、邏輯錯誤、資源未釋放等），**符合期中/期末考可能考法**。

---

## ✅ 題目 1：BMP280 溫壓感測器程式 Debug  
📁 檔案：`bmp_280.py`【出自講義 L3】

### ❓題目：
下列程式會造成「`NameError: name 'bus' is not defined`」的錯誤，請找出原因並修正。

```python
def read_bmp280_data():
    msb = bus.read_byte_data(BMP280_ADDRESS, 0xFA)
    ...
```

---

### ✅ 解答：
問題出在 `read_bmp280_data()` 被定義在 `bus = smbus2.SMBus(1)` 之前，函式內部直接使用了全域變數 `bus`，但此時尚未宣告。

#### ✅ 修改方式一（建議）：
將 `bus` 宣告移至檔案最上方，或在函式內傳入 bus：

```python
# 修改建議一：將 bus 放上來
bus = smbus2.SMBus(1)

def read_bmp280_data():
    ...
```

#### ✅ 修改方式二（參數注入）：
```python
def read_bmp280_data(bus):
    msb = bus.read_byte_data(BMP280_ADDRESS, 0xFA)
    ...
```

---

## ✅ 題目 2：播放 WAV 音檔時無聲音輸出  
📁 檔案：`1_playwav.py`【出自講義 L4】

### ❓題目：
此程式播放 `hello.wav` 檔案，但未發出聲音也不報錯，請問原因可能是什麼？該如何修正？

---

### ✅ 解答：
若系統中未安裝 `libasound.so` 或 `play` 指令，可能會無聲音輸出。  
但更常見的是：**檔案路徑錯誤或音訊設備未開啟。**

#### ✅ 修正方式：

1. **確認 hello.wav 存在於同一資料夾**
2. 若使用 Raspberry Pi，建議將 `play_wav('hello.wav')` 改為絕對路徑或確認有聲卡
3. 可加上：

```python
print("Playing hello.wav")
```

或

```python
assert os.path.exists("hello.wav"), "File not found!"
```

---

## ✅ 題目 3：語音指令測距程式失效  
📁 檔案：`L4q2.py`【出自講義 L4】

### ❓題目：
此程式執行後語音辨識與測距正常，但第二次再說話卻無反應。請問為什麼？如何修改讓它可以持續聆聽命令？

---

### ✅ 解答：
程式只執行一次 `recognize_speech()`，執行完就結束。需加入 **迴圈持續等待命令**。

#### ✅ 修改方式：
在主函式加入 while loop：

```python
if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if "measure" in command or "distance" in command:
            dist = measure_distance()
            speak_result(dist)
        else:
            print("Invalid command.")
```

---

## ✅ 題目 4：人臉閉眼偵測程式（L5q1）有錯誤  
📁 檔案：`L5q1.py`【出自講義 L5】

### ❓題目：
原程式執行後會出現 `"IndexError: index 5 is out of bounds"`。請問錯在哪裡？

---

### ✅ 解答：

臉部標記索引順序錯了！

講義順序是：
- 左眼 → index 36~41（shape[36:42]）
- 右眼 → index 42~47（shape[42:48]）

但你用的是：
```python
leftEye = shape[43:48]
rightEye = shape[37:42]
```

這會抓到錯誤點，導致 `eye[5]` 超出範圍。

#### ✅ 修正：
```python
leftEye = shape[36:42]
rightEye = shape[42:48]
```

---

## ✅ 題目 5：IMU 跌倒偵測無法亮 LED  
📁 檔案：`L3q2plus3.py`【出自講義 L3】

### ❓題目：
程式在跌倒時印出 `"FALL DETECTED!"` 但 LED 沒有亮，請檢查程式可能的錯誤原因。

---

### ✅ 解答：

雖然 `GPIO.output(LED_PIN, GPIO.HIGH)` 被呼叫，但可能的錯誤原因有：

1. 忘記設定 `LED_PIN` 為 `GPIO.OUT`
2. 忘記 `GPIO.setmode(GPIO.BCM)` 或腳位對錯
3. 沒有在程式結尾 `GPIO.cleanup()` 導致腳位被鎖定

---

### ✅ 建議補上初始化：

```python
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
```

---

這些 Debug 題可以直接作為考試用題目。如果你希望我整理成 Word 或 PDF 排版格式（含遮蔽答案版本），也可以幫你處理。是否需要？
