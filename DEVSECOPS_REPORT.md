# DevSecOps 實踐報告
## 透過靜態分析和軟體組成分析整合安全檢查

---

## 1. DevSecOps 目標介紹

### 1.1 專案概述
本報告展示了如何將輕量級安全檢查整合到開發工作流程中，通過多層次的自動化工具在開發早期發現安全性和品質問題。

### 1.2 實踐目標
- **A 級 (達成)**：透過 Linting 進行靜態程式碼分析
- **E 級 (超越)**：軟體組成分析 (SCA) 識別有漏洞的依賴套件
- **O 級 (傑出)**：進階 DevSecOps 工具整合

### 1.3 測試專案
創建了一個 Python Flask Web 應用，故意包含多種安全漏洞和程式碼品質問題：
- SQL 注入漏洞
- 命令注入漏洞
- 硬編碼密鑰
- 不安全的反序列化
- 弱加密演算法
- 過時的依賴套件

---

## 2. A 級：靜態程式碼分析 (Linting)

### 2.1 工具選擇
- **Flake8**：Python 程式碼風格檢查器
- **Pylint**：全面的程式碼分析工具

### 2.2 安裝與配置

#### 安裝命令
```bash
pip install flake8 pylint
```

#### Flake8 配置 (.flake8)
```ini
[flake8]
max-line-length = 100
max-complexity = 10
count = True
statistics = True
show-source = True
```

#### Pylint 配置 (.pylintrc)
```ini
[MASTER]
[MESSAGES CONTROL]
enable=all
[REPORTS]
output-format=text
reports=yes
score=yes
```

### 2.3 執行結果

#### Flake8 掃描結果
- **總問題數：22 個**
- **主要發現：**
  - E225/E226: 運算符周圍缺少空格 (8 個)
  - E231: 逗號後缺少空格 (7 個)
  - E402: 模組級導入位置錯誤 (3 個)
  - F401: 導入但未使用 (3 個)
  - E302: 缺少空行 (1 個)

#### 範例問題
```
app.py:108:6: E225 missing whitespace around operator
    x=1+2
     ^
utils.py:25:1: F401 'sys' imported but unused
import sys
^
```

#### Pylint 掃描結果
- **總問題數：28 個**
- **程式碼評分：6.77/10**
- **問題分類：**
  - 慣例問題 (Convention): 18 個
  - 重構建議 (Refactor): 3 個
  - 警告 (Warning): 6 個
  - 錯誤 (Error): 1 個

#### 主要發現
- 缺少函式文檔字串 (13 個)
- 錯誤的導入位置 (3 個)
- 未使用的導入 (3 個)
- 使用危險的 eval() (1 個)
- 函式參數過多 (1 個)

### 2.4 分析與討論

#### 如何預防安全性缺陷
1. **eval() 檢測**：Pylint 偵測到使用 eval()，這是代碼注入的高風險函式
2. **導入檢查**：未使用的導入可能暗示死代碼或潛在的依賴問題
3. **複雜度控制**：透過限制函式複雜度降低邏輯錯誤風險

#### 如何預防品質缺陷
1. **代碼一致性**：強制執行 PEP 8 風格指南
2. **可維護性**：檢測過長函式、過多參數等壞味道
3. **文檔完整性**：要求函式文檔字串提高代碼可讀性

---

## 3. E 級：軟體組成分析 (SCA)

### 3.1 工具選擇
- **pip-audit**：Python 官方依賴漏洞掃描工具
- **Safety**：商業級依賴安全掃描工具

### 3.2 安裝與配置

```bash
pip install pip-audit safety
```

### 3.3 執行結果

#### Safety 掃描結果
- **掃描套件數：8 個**
- **發現漏洞：73 個**
- **受影響套件：**
  - Pillow 8.1.0: 29 個漏洞
  - cryptography 3.3.2: 23 個漏洞
  - Jinja2 3.0.1: 5 個漏洞
  - Werkzeug 2.0.1: 7 個漏洞
  - urllib3 1.26.4: 5 個漏洞
  - requests 2.25.0: 3 個漏洞
  - PyYAML 5.3.1: 1 個漏洞

#### 高風險漏洞範例

**1. Pillow - CVE-2023-50447**
- **嚴重性**：高
- **影響版本**：< 10.2.0
- **描述**：任意代碼執行漏洞
- **建議**：升級至 Pillow >= 10.2.0

**2. cryptography - CVE-2023-50782**
- **嚴重性**：高
- **影響版本**：< 42.0.0
- **描述**：RSA 解密攻擊漏洞
- **建議**：升級至 cryptography >= 42.0.0

**3. Jinja2 - CVE-2024-34064**
- **嚴重性**：中
- **影響版本**：< 3.1.4
- **描述**：XSS 漏洞
- **建議**：升級至 Jinja2 >= 3.1.4

**4. requests - CVE-2024-35195**
- **嚴重性**：中
- **影響版本**：< 2.32.2
- **描述**：憑證洩漏漏洞
- **建議**：升級至 requests >= 2.32.2

### 3.4 CVSS 分數解讀

CVSS (Common Vulnerability Scoring System) 是業界標準的漏洞評分系統：

| 分數範圍 | 嚴重程度 | 行動建議 |
|---------|---------|---------|
| 9.0-10.0 | 危急 (Critical) | 立即修復 |
| 7.0-8.9 | 高 (High) | 優先修復 |
| 4.0-6.9 | 中 (Medium) | 計劃修復 |
| 0.1-3.9 | 低 (Low) | 監控觀察 |

### 3.5 供應鏈安全貢獻

#### SCA 如何保護供應鏈
1. **依賴透明度**：清楚了解所有直接和間接依賴
2. **漏洞追蹤**：即時掌握已知的安全漏洞
3. **自動化更新**：透過 Dependabot 等工具自動建議更新
4. **合規性**：符合安全標準和法規要求

#### CI/CD 管線整合

```yaml
# GitHub Actions 範例
name: Security Scan
on: [push, pull_request]

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install safety pip-audit
      - name: Run Safety
        run: safety check -r requirements.txt --json
      - name: Run pip-audit
        run: pip-audit -r requirements.txt
```

---

## 4. O 級：進階 DevSecOps 實踐

### 4.1 工具選擇
- **Semgrep**：強大的 SAST (靜態應用安全測試) 工具
- **Bandit**：Python 專門的安全漏洞掃描器

### 4.2 Semgrep - SAST 工具

#### 安裝
```bash
pip install semgrep
```

#### 自定義規則 (.semgrep.yml)
```yaml
rules:
  - id: hardcoded-secret
    pattern: $VAR = "..."
    message: Potential hardcoded secret found
    severity: WARNING
    languages: [python]

  - id: sql-injection
    pattern: cursor.execute($X)
    message: Potential SQL injection vulnerability
    severity: ERROR
    languages: [python]

  - id: command-injection
    pattern: subprocess.$FUNC(..., shell=True, ...)
    message: Command injection risk with shell=True
    severity: ERROR
    languages: [python]
```

#### 掃描結果
- **掃描檔案：3 個**
- **執行規則：5 個**
- **發現問題：14 個 (14 個阻斷性)**

#### 主要發現
1. **硬編碼密鑰** (8 個)
   - 檔案：app.py, config.py
   - 範例：`app.config['SECRET_KEY'] = 'hardcoded-secret-key-12345'`

2. **SQL 注入** (1 個)
   - 檔案：app.py:44
   - 程式碼：`cursor.execute(sql)` 使用字串拼接

3. **命令注入** (1 個)
   - 檔案：app.py:56
   - 程式碼：`subprocess.check_output(..., shell=True)`

4. **危險函式** (1 個)
   - 檔案：app.py:103
   - 程式碼：`eval()` 使用

5. **不安全反序列化** (1 個)
   - 檔案：app.py:89
   - 程式碼：`pickle.loads()`

### 4.3 Bandit - 安全掃描器

#### 安裝
```bash
pip install bandit
```

#### 掃描結果
- **掃描行數：134 行**
- **發現問題：14 個**

#### 嚴重性分佈
| 嚴重性 | 數量 | 百分比 |
|--------|------|--------|
| 高 (High) | 3 | 21.4% |
| 中 (Medium) | 4 | 28.6% |
| 低 (Low) | 7 | 50.0% |

#### 主要發現

**高嚴重性問題：**

1. **B602 - 命令注入 (CWE-78)**
   - 位置：app.py:56
   - 描述：`subprocess.check_output()` 使用 `shell=True`
   - 風險：允許攻擊者執行任意命令

2. **B201 - Flask Debug 模式 (CWE-94)**
   - 位置：app.py:125
   - 描述：Flask 在生產環境啟用 debug=True
   - 風險：暴露 Werkzeug 調試器，允許執行任意代碼

3. **B324 - 弱加密 (CWE-327)**
   - 位置：utils.py:11
   - 描述：使用 MD5 進行密碼雜湊
   - 風險：MD5 已被破解，不安全

**中嚴重性問題：**

1. **B301 - Pickle 反序列化 (CWE-502)**
   - 位置：app.py:89
   - 描述：使用 pickle.loads() 處理不可信數據

2. **B307 - eval() 使用 (CWE-78)**
   - 位置：app.py:103
   - 描述：使用危險的 eval() 函式

3. **B608 - SQL 注入 (CWE-89)**
   - 位置：app.py:43
   - 描述：字串拼接構建 SQL 查詢

4. **B104 - 綁定所有介面 (CWE-605)**
   - 位置：app.py:125
   - 描述：綁定到 0.0.0.0

### 4.4 進階工具如何增強安全態勢

#### Semgrep 優勢
1. **自定義規則**：可針對組織特定需求編寫規則
2. **精準匹配**：使用抽象語法樹 (AST) 而非正則表達式
3. **多語言支持**：支援 30+ 程式語言
4. **快速掃描**：比傳統 SAST 工具快 10-100 倍

#### Bandit 優勢
1. **Python 專門**：針對 Python 常見安全問題優化
2. **CWE 對應**：每個問題都對應到 CWE (Common Weakness Enumeration)
3. **低誤報率**：高信心度的檢測
4. **易於整合**：簡單的命令行介面

#### 與 Linting/SCA 的互補性

| 工具類型 | 檢測範圍 | 範例工具 | 互補性 |
|---------|---------|---------|--------|
| Linting | 代碼風格、品質問題 | Flake8, Pylint | 基礎品質保證 |
| SCA | 依賴漏洞 | Safety, pip-audit | 供應鏈安全 |
| SAST | 代碼邏輯漏洞 | Semgrep, Bandit | 深度安全分析 |

---

## 5. 工具比較與反思

### 5.1 工具優點總結

#### A 級工具 (Flake8 + Pylint)
**優點：**
- 快速、輕量級
- 廣泛採用，社群支持強
- 易於整合到編輯器和 CI/CD
- 幫助維持代碼一致性

**限制：**
- 主要關注風格，安全檢測有限
- 可能產生大量低優先級警告
- 需要配置來平衡嚴格性和實用性

#### E 級工具 (Safety + pip-audit)
**優點：**
- 即時更新的漏洞數據庫
- 零配置即可使用
- 清晰的修復建議
- 自動化更新整合

**限制：**
- 只檢測已知漏洞
- 無法發現自定義代碼問題
- 需要網路連接查詢數據庫
- 可能有誤報 (已修復但未更新版本號)

#### O 級工具 (Semgrep + Bandit)
**優點：**
- 深度代碼分析
- 可自定義規則
- 高準確度
- 涵蓋 OWASP Top 10

**限制：**
- 掃描時間較長
- 需要安全專業知識來解讀結果
- 可能有誤報需要手動審查
- 規則維護需要持續投入

### 5.2 整體反思

#### 成功之處
1. **分層防禦**：三個等級的工具提供多層次保護
2. **早期發現**：在開發階段而非生產環境發現問題
3. **自動化**：所有工具都可自動化，減少人工成本
4. **教育價值**：工具輸出幫助開發人員學習安全最佳實踐

#### 挑戰與限制
1. **誤報管理**：需要投入時間區分真正的問題和誤報
2. **工具疲勞**：過多工具可能導致開發人員忽視警告
3. **維護負擔**：規則和配置需要持續更新
4. **文化變革**：需要組織文化支持「安全左移」

#### 最佳實踐建議
1. **漸進採用**：從 A 級開始，逐步引入更高級工具
2. **整合 CI/CD**：在提交和 PR 階段自動運行
3. **設定基準線**：接受現有代碼的問題，專注於新代碼
4. **定期審查**：定期檢視和更新規則配置
5. **團隊培訓**：確保團隊理解工具輸出並知道如何修復

---

## 6. CI/CD 整合範例

### 6.1 完整管線設計

```yaml
name: DevSecOps Pipeline

on: [push, pull_request]

jobs:
  code-quality:
    name: Code Quality (A 級)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'

      - name: Install linting tools
        run: pip install flake8 pylint

      - name: Run Flake8
        run: flake8 . --count --statistics
        continue-on-error: true

      - name: Run Pylint
        run: pylint **/*.py --exit-zero

  dependency-scan:
    name: Dependency Scan (E 級)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install SCA tools
        run: pip install safety pip-audit

      - name: Run Safety
        run: safety check -r requirements.txt --output json
        continue-on-error: true

      - name: Run pip-audit
        run: pip-audit -r requirements.txt
        continue-on-error: true

  security-scan:
    name: Security Scan (O 級)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install security tools
        run: pip install semgrep bandit

      - name: Run Semgrep
        run: semgrep --config=auto --json --output=semgrep.json .

      - name: Run Bandit
        run: bandit -r . -f json -o bandit.json

      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: security-reports
          path: |
            semgrep.json
            bandit.json
```

### 6.2 GitLab CI 範例

```yaml
stages:
  - lint
  - sca
  - sast

linting:
  stage: lint
  script:
    - pip install flake8 pylint
    - flake8 . --count --statistics
    - pylint **/*.py --exit-zero

dependency-check:
  stage: sca
  script:
    - pip install safety
    - safety check -r requirements.txt --json

security-scan:
  stage: sast
  script:
    - pip install semgrep bandit
    - semgrep --config=auto .
    - bandit -r . -f json
```

---

## 7. 參考資料與工具文件

### 7.1 工具官方文件

#### A 級工具
- **Flake8**: https://flake8.pycqa.org/
- **Pylint**: https://pylint.pycqa.org/

#### E 級工具
- **pip-audit**: https://pypi.org/project/pip-audit/
- **Safety**: https://docs.safetycli.com/
- **GitHub Dependabot**: https://docs.github.com/en/code-security/dependabot

#### O 級工具
- **Semgrep**: https://semgrep.dev/docs/
- **Bandit**: https://bandit.readthedocs.io/

### 7.2 安全標準與框架
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **CWE (Common Weakness Enumeration)**: https://cwe.mitre.org/
- **CVSS (Common Vulnerability Scoring System)**: https://www.first.org/cvss/
- **NIST Secure SDLC**: https://csrc.nist.gov/projects/ssdf

### 7.3 DevSecOps 資源
- **DevSecOps Manifesto**: https://www.devsecops.org/
- **OWASP DevSecOps Guideline**: https://owasp.org/www-project-devsecops-guideline/
- **GitHub Security Lab**: https://securitylab.github.com/

### 7.4 學習資源
- **Python Security Best Practices**: https://snyk.io/blog/python-security-best-practices/
- **SAST vs DAST vs SCA**: https://www.synopsys.com/glossary/what-is-sast.html

---

## 8. 附錄：掃描結果統計

### 8.1 總體發現統計

| 工具 | 檢測類型 | 發現問題數 | 高嚴重性 | 中嚴重性 | 低嚴重性 |
|------|---------|-----------|---------|---------|---------|
| Flake8 | 代碼風格 | 22 | - | - | 22 |
| Pylint | 代碼品質 | 28 | 1 | 6 | 21 |
| Safety | 依賴漏洞 | 73 | 多個 | 多個 | 多個 |
| Semgrep | SAST | 14 | 3 | 6 | 5 |
| Bandit | 安全掃描 | 14 | 3 | 4 | 7 |
| **總計** | - | **151** | **7+** | **16+** | **55+** |

### 8.2 問題分類

#### 安全問題
- SQL 注入: 1
- 命令注入: 1
- 代碼注入 (eval): 1
- 不安全反序列化: 1
- 硬編碼密鑰: 8
- 弱加密: 1
- Debug 模式啟用: 1
- 依賴漏洞: 73

#### 品質問題
- 代碼風格: 22
- 缺少文檔: 13
- 未使用導入: 3
- 複雜度過高: 1

### 8.3 修復優先級建議

**P0 (立即修復)：**
1. 命令注入漏洞 (app.py:56)
2. SQL 注入漏洞 (app.py:43)
3. Debug 模式啟用 (app.py:125)
4. 升級 cryptography 至 >= 42.0.0
5. 升級 Pillow 至 >= 10.2.0

**P1 (本週修復)：**
1. 移除 eval() 使用
2. 替換 pickle 為安全的序列化方法
3. 移除硬編碼密鑰，使用環境變數
4. 升級其他有漏洞的依賴

**P2 (計劃修復)：**
1. 修復所有 Pylint 警告
2. 改善代碼文檔
3. 重構高複雜度函式

---

## 9. 結論

本實踐成功展示了如何通過多層次的自動化工具實現 DevSecOps 原則。透過整合靜態分析 (Linting)、軟體組成分析 (SCA) 和安全應用測試 (SAST)，我們能夠：

1. **早期發現問題**：在開發階段而非生產環境識別安全和品質問題
2. **分層防禦**：不同類型的工具提供互補的保護
3. **自動化流程**：所有檢查都可整合到 CI/CD 管線
4. **持續改進**：建立安全和品質的回饋循環

### 關鍵要點
- DevSecOps 不是單一工具，而是工具、流程和文化的結合
- 自動化是可擴展安全的關鍵
- 沒有完美的工具，需要組合使用
- 教育和培訓與工具同等重要

### 下一步
1. 將這些工具整合到實際專案的 CI/CD 管線
2. 建立安全冠軍文化，培養團隊安全意識
3. 定期審查和更新安全策略
4. 探索更多進階工具 (DAST、容器掃描等)

---

**報告生成日期**：2025-11-18
**專案位置**：c:\_AG10
**工具版本**：
- Python: 3.12
- Flake8: 最新版本
- Pylint: 最新版本
- Safety: 3.7.0
- Semgrep: 最新版本
- Bandit: 1.9.1
