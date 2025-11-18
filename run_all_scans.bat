@echo off
REM DevSecOps 掃描腳本 - 運行所有安全和品質檢查

echo ========================================
echo DevSecOps 自動化掃描工具
echo ========================================
echo.

echo [1/6] 安裝所有必要的工具...
pip install flake8 pylint pip-audit safety semgrep bandit --quiet
echo ✓ 工具安裝完成
echo.

echo [2/6] 運行 Flake8 (代碼風格檢查)...
flake8 app.py config.py utils.py --statistics --count > flake8_report.txt 2>&1
echo ✓ Flake8 掃描完成 - 結果保存至 flake8_report.txt
echo.

echo [3/6] 運行 Pylint (代碼品質分析)...
pylint app.py config.py utils.py --output-format=text > pylint_report.txt 2>&1
echo ✓ Pylint 掃描完成 - 結果保存至 pylint_report.txt
echo.

echo [4/6] 運行 Safety (依賴漏洞掃描)...
safety check -r requirements.txt --output text > safety_report.txt 2>&1
echo ✓ Safety 掃描完成 - 結果保存至 safety_report.txt
echo.

echo [5/6] 運行 Semgrep (SAST 安全分析)...
semgrep --config .semgrep.yml app.py config.py utils.py > semgrep_simple_report.txt 2>&1
echo ✓ Semgrep 掃描完成 - 結果保存至 semgrep_simple_report.txt
echo.

echo [6/6] 運行 Bandit (Python 安全掃描)...
bandit -r . -f txt -o bandit_report.txt 2>&1
bandit -r . -f json -o bandit_report.json 2>&1
echo ✓ Bandit 掃描完成 - 結果保存至 bandit_report.txt 和 bandit_report.json
echo.

echo ========================================
echo 所有掃描完成！
echo ========================================
echo.
echo 生成的報告檔案：
echo   - flake8_report.txt       (A級: 代碼風格)
echo   - pylint_report.txt       (A級: 代碼品質)
echo   - safety_report.txt       (E級: 依賴漏洞)
echo   - semgrep_simple_report.txt (O級: SAST分析)
echo   - bandit_report.txt       (O級: 安全掃描)
echo   - bandit_report.json      (O級: JSON格式)
echo.
echo 請查看 DEVSECOPS_REPORT.md 了解詳細分析
echo 使用 SUBMISSION_GUIDE.md 了解如何轉換為 PDF
echo.
pause
