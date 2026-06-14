# auto_CICD — Claude 工作規則

## 專案簡介
Black-Scholes 選擇權計算機，用來 demo GitHub Actions CI/CD 流程。

## 專案結構
- `bs_model.py` — BS Model 核心計算（call/put price + Greeks）
- `app.py` — Flask web app
- `freeze.py` — 將 Flask 凍結成靜態 HTML 供 GitHub Pages 部署
- `tests/test_bs_model.py` — BS 數學邏輯測試（13個）
- `tests/test_app.py` — Flask 路由測試（4個）
- `.github/workflows/ci-cd.yml` — CI/CD pipeline

## 常用指令
```powershell
# 安裝依賴
pip install -r requirements.txt

# 本地跑 Flask
python app.py

# 跑測試
pytest tests/ -v

# 產生靜態檔
python freeze.py
```

## CI/CD 流程
```
git push
    └── GitHub Actions 觸發
            ├── [CI] pytest tests/ -v        # 17 個測試全過才繼續
            └── [CD] python freeze.py
                      └── 部署到 GitHub Pages
```

## Push 後必做
push 完一定要用 gh CLI 確認 Actions 狀態：
```powershell
gh run list --limit 3
# 失敗時
gh run view <run-id> --log-failed
```

## 注意事項
- GitHub Pages 是靜態網站，不支援 POST，計算邏輯用 JavaScript 在前端執行
- `conftest.py` 放在根目錄，讓 pytest 能 import `app` 和 `bs_model`
- 測試改 HTML 結構時，記得同步更新 `test_app.py` 的斷言（`id=` vs `name=`）
