根據你提供的講義 **《Lect2. read sensing data (2025).2》**，我為你精選設計了 **三題可能會出現在小考或期中考的題目**，**完全不超出講義範圍**，並附上**標準解答**：

---

## 📘 題目一【觀念題】  
**請說明 HC-SR04 超音波感測器的運作原理，並說明如何使用其輸出腳位計算距離。**

### ✅ 解答：

1. HC-SR04 感測器的運作流程如下：

   1️⃣ `Trig` 腳輸入 10 微秒的高電位脈衝  
   2️⃣ 感測器發出 8 個 40kHz 的超音波  
   3️⃣ 超音波碰到物體反射回來  
   4️⃣ `Echo` 腳從低轉高，持續到聲波回來為止  
   5️⃣ `Echo` 腳保持高電位的時間長度表示來回時間

2. 距離計算公式為：

\[
\text{距離 (cm)} = \frac{\text{時間（秒）} \times \text{聲速（m/s）}}{2} \times 100
\]

其中聲速通常取 343 m/s（攝氏 20°C），乘以 100 是換算成公分，除以 2 是因為有來回路徑。

---

## 📘 題目二【電學計算題】  
**若 Raspberry Pi 的 GPIO 輸出為 3.3V，LED 正向電壓為 1.85V，需求電流為 20mA，請計算最低所需電阻值以保護 LED。**

### ✅ 解答：

使用歐姆定律 \( R = \frac{V}{I} \)

\[
R = \frac{3.3 - 1.85}{0.02} = \frac{1.45}{0.02} = 72.5\ \Omega
\]

✅ 為避免燒毀 LED，應使用大於或等於 **72.5Ω** 的電阻，一般常用 **100Ω ~ 1KΩ**。

---

## 📘 題目三【程式概念題】  
**請說明下列 GPIO Python 程式的執行流程，並指出其中的錯誤處理與清理邏輯。**

```python
import RPi.GPIO as GPIO
import time

LED_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        print("LED on")
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
```

### ✅ 解答：

1. `GPIO.setmode(GPIO.BOARD)`：設定為物理腳位編號模式（z字形排列）

2. 將 `LED_PIN` 腳位設為輸出模式

3. 在 `try` 迴圈中持續以每秒頻率開關 LED（1秒亮、1秒滅）

4. 當使用者按下 Ctrl+C（拋出 `KeyboardInterrupt`）時，會印出 `Interrupted by user`

5. 不論是否發生錯誤，`finally` 區塊都會執行 → 關閉 LED 並呼叫 `GPIO.cleanup()` 做腳位清理，避免重複使用腳位出錯
