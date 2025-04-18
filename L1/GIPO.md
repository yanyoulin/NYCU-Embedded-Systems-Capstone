當然可以！這裡是針對 Raspberry Pi 上常用的 `RPi.GPIO` 函式庫所做的完整整理，並說明何時應該將 GPIO 設為輸出（OUT）或輸入（IN），非常適合用來複習、備考，或實作專題時快速參考。

---

## 🧠 一、什麼是 GPIO？

**GPIO（General Purpose Input/Output）** 是一種可以自由設定為「輸入」或「輸出」的萬用腳位，通常用來控制 LED、馬達、按鈕、感測器、蜂鳴器等電子元件。

---

## 📌 二、常用 GPIO 函式總表（使用 `RPi.GPIO` 模組）

先引入模組：
```python
import RPi.GPIO as GPIO
```

---

### 1️⃣ `GPIO.setmode(...)`

設定腳位編號方式：

```python
GPIO.setmode(GPIO.BOARD)   # 使用實體腳位編號（1~40）
GPIO.setmode(GPIO.BCM)     # 使用 GPIO 號碼（如 GPIO17）
```

> ✅ 推薦使用 BCM，對照電路圖與參考資料較方便。

---

### 2️⃣ `GPIO.setup(pin, mode)`

設定腳位模式為輸入或輸出：

```python
GPIO.setup(18, GPIO.OUT)  # 設定 GPIO18 為輸出模式（控制 LED）
GPIO.setup(23, GPIO.IN)   # 設定 GPIO23 為輸入模式（接收按鈕訊號）
```

可搭配 pull-up/down 電阻：
```python
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # 上拉電阻
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 下拉電阻
```

---

### 3️⃣ `GPIO.output(pin, value)`

寫入高/低電位（僅限 OUT 模式）：

```python
GPIO.output(18, GPIO.HIGH)   # 輸出高電位（3.3V）
GPIO.output(18, GPIO.LOW)    # 輸出低電位（0V）
```

也可以用 `True/False` 表示：
```python
GPIO.output(18, True)
```

---

### 4️⃣ `GPIO.input(pin)`

讀取輸入腳位的狀態（僅限 IN 模式）：

```python
val = GPIO.input(23)
if val == GPIO.HIGH:
    print("按鈕被按下！")
```

---

### 5️⃣ `GPIO.cleanup()`

在程式結束前釋放 GPIO 腳位資源，避免占用或錯誤：

```python
GPIO.cleanup()
```

通常放在：
```python
try:
    ...
except KeyboardInterrupt:
    GPIO.cleanup()
```

---

## 🧩 三、什麼情況用 `OUT`，什麼情況用 `IN`？

| 模式 | 使用情境 | 範例元件 | 使用函式 |
|------|-----------|----------|-----------|
| `GPIO.OUT` | 你要「控制」某東西 | LED、蜂鳴器、繼電器、馬達控制腳位 | `GPIO.output()` |
| `GPIO.IN`  | 你要「讀取」某東西 | 按鈕、紅外線感測器、溫濕度資料腳 | `GPIO.input()` |

---

### 🔧 常見例子

- **控制 LED（OUT）**：
```python
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)  # 亮
```

- **讀取按鈕（IN）**：
```python
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
if GPIO.input(23) == GPIO.LOW:
    print("按鈕按下了！")
```

---

## ✅ 四、完整範例：按鈕控制 LED

```python
import RPi.GPIO as GPIO
import time

LED_PIN = 18
BTN_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(BTN_PIN) == GPIO.LOW:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

---

是否需要我幫你整理成表格版或 PDF？或你想試著接蜂鳴器、繼電器、超音波模組，我也可以教你腳位怎麼接＋程式怎麼寫。需要嗎？
