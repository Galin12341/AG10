# DevSecOps 工具手動執行指南
## 逐步執行與截圖教學

---

## 準備工作

### 1. 安裝所有工具
```bash
pip install flake8 pylint pip-audit safety semgrep bandit
```

💡 **截圖建議**：安裝完成後截圖顯示版本資訊

---

## A 級：靜態程式碼分析

### 步驟 1：執行 Flake8

#### 基本掃描
```bash
flake8 app.py config.py utils.py
```

#### 帶統計資訊的掃描（推薦）
```bash
flake8 app.py config.py utils.py --statistics --count --show-source
```

#### 參數說明：
- `--statistics`: 顯示錯誤類型統計
- `--count`: 顯示總錯誤數
- `--show-source`: 顯示出錯的原始碼

📸 **截圖要點**：
- 捕捉顯示錯誤的終端輸出
- 確保可以看到檔案名、行號、錯誤類型
- 底部的統計資訊

#### 只掃描特定檔案
```bash
# 只掃描 app.py
flake8 app.py --statistics

# 掃描所有 Python 檔案
flake8 . --statistics
```

---

### 步驟 2：執行 Pylint

#### 基本掃描
```bash
pylint app.py config.py utils.py
```

#### 帶詳細報告的掃描（推薦）
```bash
pylint app.py config.py utils.py --reports=yes
```

#### 只看特定類型的問題
```bash
# 只看錯誤和警告
pylint app.py --disable=C,R

# C=Convention, R=Refactor, W=Warning, E=Error
```

📸 **截圖要點**：
- 捕捉問題列表
- 捕捉底部的評分（例如：6.77/10）
- 捕捉統計表格

#### 查看特定檔案的詳細分析
```bash
pylint app.py --reports=yes --output-format=text
```

---

## E 級：軟體組成分析

### 步驟 3：執行 Safety

#### 基本掃描
```bash
safety check -r requirements.txt
```

#### 帶完整資訊的掃描（推薦）
```bash
safety check -r requirements.txt --full-report
```

📸 **截圖要點**：
- 捕捉 Safety 的 ASCII 藝術 logo
- 捕捉漏洞摘要（發現 73 個漏洞）
- 捕捉 2-3 個具體漏洞範例，包含：
  - 套件名稱和版本
  - CVE 編號
  - 漏洞描述
  - 建議升級版本

#### 查看特定嚴重性的漏洞
```bash
# 只看高危漏洞（需要付費版本）
# 免費版會顯示所有漏洞
safety check -r requirements.txt
```

#### 產生 JSON 格式報告
```bash
safety check -r requirements.txt --json
```

---

### 步驟 4：執行 pip-audit

#### 基本掃描
```bash
pip-audit -r requirements.txt
```

#### 帶詳細資訊的掃描
```bash
pip-audit -r requirements.txt --desc
```

📸 **截圖要點**：
- 如果成功執行，捕捉漏洞列表
- 如果有錯誤，也可以截圖說明遇到的問題

💡 **注意**：pip-audit 在某些環境可能會有問題，這是正常的。可以專注於 Safety 的結果。

---

## O 級：進階安全工具

### 步驟 5：執行 Semgrep

#### 使用自定義規則掃描
```bash
semgrep --config .semgrep.yml app.py config.py utils.py
```

#### 使用官方規則庫（需要網路）
```bash
# 使用 Python 安全規則
semgrep --config "p/python" app.py config.py utils.py

# 使用 OWASP Top 10 規則
semgrep --config "p/owasp-top-ten" app.py config.py utils.py
```

📸 **截圖要點**：
- 捕捉掃描摘要（Scan Summary）
- 捕捉發現的問題列表（14 findings）
- 捕捉具體問題範例：
  - SQL 注入 (app.py:44)
  - 命令注入 (app.py:56)
  - eval 使用 (app.py:103)
  - 硬編碼密鑰

#### 只掃描特定嚴重性
```bash
# 只看 ERROR 級別
semgrep --config .semgrep.yml --severity ERROR app.py
```

---

### 步驟 6：執行 Bandit

#### 基本掃描
```bash
bandit -r .
```

#### 帶詳細資訊的掃描（推薦）
```bash
bandit -r . -v
```

#### 只顯示高嚴重性問題
```bash
bandit -r . -ll
# -ll = 只顯示 Low 以上（Medium 和 High）
# -lll = 只顯示 High
```

📸 **截圖要點**：
- 捕捉掃描摘要
- 捕捉嚴重性統計：
  - High: 3 個
  - Medium: 4 個
  - Low: 7 個
- 捕捉 2-3 個高嚴重性問題範例：
  - B602: 命令注入
  - B201: Flask debug=True
  - B324: MD5 弱加密

#### 查看特定檔案的問題
```bash
bandit app.py -v
```

#### 產生 HTML 報告（方便查看）
```bash
bandit -r . -f html -o bandit_report.html
```
然後用瀏覽器打開 bandit_report.html 截圖。

---

## 比較和學習

### 查看不同工具如何檢測相同問題

#### 例子 1：檢測 eval() 使用 (app.py:103)

**Pylint:**
```bash
pylint app.py | grep eval
```
輸出：`W0123: Use of eval (eval-used)`

**Semgrep:**
```bash
semgrep --config .semgrep.yml app.py | grep -A 3 eval
```

**Bandit:**
```bash
bandit app.py | grep -A 5 B307
```

📸 **截圖建議**：並排比較三個工具對同一問題的報告

---

#### 例子 2：檢測硬編碼密鑰

**所有工具一起運行：**
```bash
echo "=== Semgrep ==="
semgrep --config .semgrep.yml config.py | grep -A 2 "hardcoded"

echo "=== Bandit ==="
bandit config.py | grep -A 3 B105
```

---

## 逐步截圖清單

### A 級截圖（4-5 張）
- [ ] Flake8 安裝和版本確認
- [ ] Flake8 掃描輸出（顯示錯誤）
- [ ] Flake8 統計資訊
- [ ] Pylint 掃描輸出（顯示問題）
- [ ] Pylint 評分和統計表

### E 級截圖（3-4 張）
- [ ] Safety 掃描摘要（73 個漏洞）
- [ ] Safety 具體漏洞範例（2-3 個）
- [ ] Safety CVE 詳細資訊
- [ ] pip-audit 結果（可選）

### O 級截圖（4-5 張）
- [ ] Semgrep 掃描摘要
- [ ] Semgrep 發現的安全問題
- [ ] Bandit 嚴重性統計
- [ ] Bandit 高危問題詳情
- [ ] Bandit HTML 報告（可選）

---

## 進階技巧

### 1. 將輸出保存到檔案同時顯示在螢幕上
```bash
# Windows PowerShell
flake8 app.py --statistics | Tee-Object -FilePath flake8_output.txt

# Linux/Mac 或 Git Bash
flake8 app.py --statistics | tee flake8_output.txt
```

### 2. 只看特定類型的問題
```bash
# Flake8: 只看導入相關問題
flake8 . | grep "F401\|F403\|F405"

# Bandit: 只看 SQL 相關問題
bandit -r . | grep -A 5 "B608"
```

### 3. 產生彩色輸出（更適合截圖）
```bash
# Pylint 帶顏色
pylint app.py --output-format=colorized

# Bandit 預設就有顏色
bandit -r .
```

### 4. 比較修復前後的差異
```bash
# 修復前
flake8 app.py > before.txt

# 修復一些問題後
flake8 app.py > after.txt

# 比較
diff before.txt after.txt
```

---

## 截圖最佳實踐

### Windows 截圖工具
- **Snipping Tool** (Win + Shift + S)
- **PowerShell 截圖**
- **第三方工具**: ShareX, Greenshot

### 截圖技巧
1. **調整終端大小**：確保重要資訊都在螢幕內
2. **使用深色主題**：對比度更高，更易閱讀
3. **放大字體**：確保文字清晰可讀
4. **完整截圖**：包含命令和輸出
5. **標註重點**：用箭頭或框框標示關鍵資訊

### 終端美化
```bash
# 設定更大的字體
# 在 PowerShell/CMD 屬性中調整

# 使用彩色輸出
# 大多數工具預設支援彩色
```

---

## 學習要點

### 每個工具的重點

**Flake8:**
- 學習 PEP 8 編碼風格
- 理解不同錯誤代碼 (E, F, W)
- 認識常見的代碼異味

**Pylint:**
- 理解代碼品質評分
- 學習重構建議
- 認識代碼複雜度問題

**Safety:**
- 學習 CVE 編號系統
- 理解 CVSS 評分
- 認識供應鏈安全

**Semgrep:**
- 學習 SAST 工作原理
- 理解抽象語法樹 (AST)
- 認識常見安全模式

**Bandit:**
- 學習 CWE 分類
- 理解安全嚴重性等級
- 認識 Python 特定的安全問題

---

## 快速命令參考

```bash
# A 級
flake8 app.py config.py utils.py --statistics --count
pylint app.py config.py utils.py --reports=yes

# E 級
safety check -r requirements.txt
pip-audit -r requirements.txt

# O 級
semgrep --config .semgrep.yml app.py config.py utils.py
bandit -r . -v
```

---

## 常見問題排查

### 問題 1: pip-audit 失敗
**解決方案**: 使用 Safety 即可，它提供類似功能

### 問題 2: Semgrep 編碼錯誤
**解決方案**: 使用本地規則檔案 `.semgrep.yml` 而不是 `--config=auto`

### 問題 3: 輸出太多無法截圖
**解決方案**:
```bash
# 只看前 20 行
flake8 app.py | head -20

# 只看特定檔案
pylint app.py
```

---

祝你學習愉快！逐步執行這些命令將幫助你深入理解 DevSecOps 工具的工作原理。
