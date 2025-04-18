這份 `10dof_imu_reading.py` 是一個**完整控制 ICM-20948 + AK09916 的驅動程式與即時數據印出腳本**，整體結構嚴謹，涵蓋：

- ✅ 註冊初始化與 bank 管理  
- ✅ 加速度計 / 陀螺儀 / 磁力計資料讀取  
- ✅ 傳感器校準與設置  
- ✅ 數據單位轉換  
- ✅ 實時讀取與印出 9 軸感測資料  

我將依照模組區塊與功能進行**逐段詳細解說**，補上背景概念與注意事項。

---

## 📦 第一段：常數定義與暫存器位址

```python
CHIP_ID = 0xEA
I2C_ADDR = 0x68
...
ICM20948_ACCEL_XOUT_H = 0x2D
...
AK09916_I2C_ADDR = 0x0c
...
AK09916_CNTL2 = 0x31
```

這段定義了所有重要的暫存器與常數，包括：
- ICM20948：內建加速度、陀螺儀、溫度感測器
- AK09916：外接的 3 軸磁力計（由 ICM20948 的 I²C master 控制）

這些常數幫助我們能以更直覺的方式操作特定功能，而不用直接寫位址數值。

---

## 🔧 第二段：ICM20948 類別實作（驅動本體）

這個類別實作了所有與感測器溝通的功能。

---

### 🔹 2-1. I²C 操作基本方法：

```python
def write(self, reg, value)
def read(self, reg)
def read_bytes(self, reg, length)
```

- 對指定 `reg` 地址進行單一寫入、讀取或多位元組讀取。
- 用於操控暫存器內容、傳送指令、讀資料。

---

### 🔹 2-2. Bank 切換與磁力計觸發

```python
def bank(self, value)
def trigger_mag_io(self)
```

- **ICM20948 採用 bank 系統**（bank0 ~ bank3），同一個地址會依據 bank 有不同功能。
- `bank()` 負責切換 register group。
- `trigger_mag_io()` 會啟用一次磁力計的主控 I²C 傳輸（需寫兩次 USER_CTRL）

---

### 🔹 2-3. AK09916 操作函式

```python
def mag_write()
def mag_read()
def mag_read_bytes()
```

這些函式使用 ICM20948 作為 I²C Master 去存取 AK09916（磁力計）：
- 設定 slave address、register address、寫入值
- 切回 bank 0 再觸發 IO，才能實際送出命令

---

### 🔹 2-4. `read_magnetometer_data()` 實作邏輯

```python
self.mag_write(AK09916_CNTL2, 0x01)  # 觸發單次讀取
...
while not self.magnetometer_ready()
...
x, y, z = struct.unpack("<hhh", data)
x *= 0.15
```

- 向 CNTL2 寫 `0x01` 表示要進行一次量測（single mode）
- 等待 `ST1` 中的 DRDY（資料準備完成）
- 讀出 6 bytes（每軸 16-bit，小端序），並乘以 0.15 得到 μT

---

### 🔹 2-5. `read_accelerometer_gyro_data()`

```python
data = self.read_bytes(ICM20948_ACCEL_XOUT_H, 12)
ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))
```

- 讀取 12 bytes：加速度與陀螺儀（每軸 16-bit，大端序）
- 根據加速度 full scale（±2g, 4g, 8g, 16g）對原始值進行單位轉換
- 同理轉換陀螺儀為 deg/s（根據 ±250, 500, 1000, 2000 dps）

轉換比例如下：

| 範圍 | 對應比例（g） |
|------|---------------|
| ±2g  | 16384.0       |
| ±4g  | 8192.0        |
| ±8g  | 4096.0        |
| ±16g | 2048.0        |

---

### 🔹 2-6. 設定感測器參數（Rate、範圍、濾波）

```python
set_accelerometer_sample_rate()
set_accelerometer_full_scale()
set_accelerometer_low_pass()
...
set_gyro_sample_rate()
...
```

- 對應設定加速度與陀螺儀的取樣頻率、範圍與低通濾波器
- 使用位元運算來更新暫存器內容

範例：
```python
rate = int((1125 / target_rate) - 1)
```
這是根據 datasheet 所述，設定 divider 來達成對應的 sample rate。

---

### 🔹 2-7. 溫度讀取

```python
temp_raw = struct.unpack(">h", ...)[0]
temperature = ((raw - offset) / sensitivity) + degrees_offset
```

- 從 TEMP_OUT_H/L 讀兩個 bytes
- 使用公式將原始值轉為攝氏溫度，單位為 °C

---

### 🔹 2-8. `__init__()` 初始化過程

這是整支驅動的核心啟動流程：

- 開啟 I²C bus
- 切到 bank 0，確認 WHO_AM_I 為 `0xEA`
- Reset + 啟動
- 設定 sample rate、scale、濾波器
- 開啟 I²C master mode
- 初始化 AK09916，確認其 WHO_AM_I 並 reset

---

## 🧪 主程式區塊 `if __name__ == "__main__":`

```python
imu = ICM20948()

while True:
    mx, my, mz = imu.read_magnetometer_data()
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    ...
```

- 創建 `ICM20948` 物件並初始化所有設定
- 每次迴圈：
  - 讀取磁力計、加速度計、陀螺儀資料
  - 印出成六軸資訊（加速度 + 角速度 + 磁力）
- 每 0.25 秒更新一次

輸出格式範例如：

```
Accel:  0.00  -0.02   1.01
Gyro:   0.15   0.00  -0.30
Mag:    3.45   1.22   0.56
```

---

## ✅ 總結功能表

| 功能 | 說明 |
|------|------|
| 加速度/角速度 | 使用 bank 0 寄存器，結合比例轉為物理單位 |
| 磁力資料 | 經過 master I²C 控制 AK09916，完成完整讀取 |
| 設定控制 | 包含 sample rate、FSR、LPF 設定 |
| 實時顯示 | 以 `print()` 每 0.25 秒印出感測值 |

---

是否需要我幫你改寫成更進階的形式，例如：
- ✨ 寫入 CSV 記錄資料
- 📈 使用 matplotlib 即時畫圖
- 🧭 計算 heading 角（電子羅盤）
- 🚨 判斷跌倒、翻滾等事件

都可以幫你加上！需要嗎？
