根據你提供的講義《Lect1. PI intro, install, GPIO》，如果教授只會從這份講義出題，以下是我根據其內容設計出的三題可能考題，每題都附有完整解答，涵蓋以下三個重要面向：<br>

Raspberry Pi 系統安裝流程與設定<br>

Headless 模式的概念與應用<br>

GPIO 基本原理與使用限制<br>

📘 題目一：請簡述 Raspberry Pi 使用 USB-to-TTL 傳輸線進行 Headless 安裝的流程。<br>
✅ 解答：<br>
準備 SD 卡與系統映像檔：<br>

使用 SD Formatter 格式化 SD 卡<br>

使用 balenaEtcher 或 Raspberry Pi Imager 將 Raspbian 映像檔寫入<br>

編輯開機檔案（/boot）：<br>

建立空白檔案 ssh 來開啟 SSH 功能<br>

建立 userconf.txt 並放入格式為 帳號:加密密碼<br>

準備硬體：<br>

使用 USB-to-TTL 傳輸線連接 PC 與 Raspberry Pi（TX、RX、GND）<br>

開啟 Raspberry Pi：<br>

插入 SD 卡並接上電源<br>

使用 PC 上的終端機軟體（如 MobaXterm）透過序列埠登入<br>

📘 題目二：什麼是 Headless 操作？為何在嵌入式系統開發中常採用此方式？<br>
✅ 解答：<br>
Headless 操作指的是在沒有螢幕、鍵盤與滑鼠的情況下操作系統或裝置。<br>

在 Raspberry Pi 或其他嵌入式系統中，常用 SSH 或 USB-to-TTL 進行 Headless 操作。<br>

優點：<br>

減少硬體需求與成本

可用遠端方式大量部署與控制設備

適合狹小或封閉空間的設備

增加自動化與靈活性

📘 題目三：請列出 Raspberry Pi GPIO 的三項電氣限制，並說明不遵守可能會造成的後果。<br>
✅ 解答：<br>
不得輸入超過 3.3V 的訊號：<br>

GPIO 接收電壓上限為 3.3V，超過會損壞 CPU I/O 腳位。

不得給予超過 5V 電源：

若從非標準電源（如 USB 充電器）輸入超過 5V 可能損壞整機。

不可在通電時使用金屬物品（如螺絲起子）碰觸 GPIO：

容易造成短路，燒毀電路板。

