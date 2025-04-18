根據你提供的第三週講義《Lect3. process data (2025).1》，我從中設計出三題可能會在課堂小考或作業中出現的題目，**完全不超出講義範圍**，涵蓋：

- 感測器資料應用（壓力→高度、加速度→距離、角速度→旋轉角）
- 設定/校正 IMU
- 判斷與應用程式設計邏輯（如跌倒偵測）

---

## 📘 題目一【計算題】  
**請說明如何透過 BMP280 感測器讀得的氣壓值計算對應的高度？並假設目前測得壓力為 100325 Pa，計算其對應高度（使用標準海平面壓力為 101325 Pa）。**

---

### ✅ 解答：

使用講義第 13 頁公式：

\[
\text{altitude} = \left(1 - \left(\frac{P}{P_0}\right)^{\frac{1}{5.255}}\right) \times 44330
\]

其中：
- \(P = 100325 \, \text{Pa}\)
- \(P_0 = 101325 \, \text{Pa}\)（標準海平面氣壓）

---

代入：

\[
\frac{P}{P_0} = \frac{100325}{101325} \approx 0.9901
\]

\[
\left(0.9901\right)^{\frac{1}{5.255}} \approx 0.9981
\]

\[
\text{altitude} = (1 - 0.9981) \times 44330 \approx 84.3 \, \text{m}
\]

---

### ✅ 最後答案：高度約 **84.3 公尺**

---

## 📘 題目二【程式概念題】  
**請簡述如何根據 IMU 加速度與陀螺儀資料計算：**

1. 移動距離（distance）  
2. 旋轉角度（rotation angle）

---

### ✅ 解答：

1. **距離計算公式**（講義第 33 頁）：

\[
v = v_0 + at,\quad s = v_0t + \frac{1}{2}at^2
\]

- 需進行 offset 校正（acc = acc_raw - offset）
- 每一小段時間（如 0.25 秒）更新速度與位移

---

2. **旋轉角度公式**（講義第 34 頁）：

\[
\theta = \theta_0 + \omega \cdot t
\]

- 由陀螺儀的 angular velocity 乘以時間積分而得
- 同樣需要校正：gyro_calibrated = gyro_raw - offset

---

## 📘 題目三【應用實作題】  
**請簡述跌倒偵測的基本邏輯，並寫出如何透過 Python 計算 total acceleration 來觸發 LED。**

---

### ✅ 解答：

### ▸ 跌倒偵測邏輯：

- 利用總加速度變化來判斷是否跌倒
- 通常定義總加速度如下：

\[
\text{total\_acc} = \sqrt{a_x^2 + a_y^2 + a_z^2}
\]

- 若 `total_acc > 2.5` 或 `< 0.5`，視為可能發生跌倒

---

### ▸ Python 範例：

```python
import math
total_acc = math.sqrt(ax**2 + ay**2 + az**2)

if total_acc > 2.5 or total_acc < 0.5:
    GPIO.output(LED_PIN, GPIO.HIGH)
else:
    GPIO.output(LED_PIN, GPIO.LOW)
```
