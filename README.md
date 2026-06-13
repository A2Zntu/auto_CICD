# auto_CICD — GitHub Actions CI/CD Demo

每次 push 到 GitHub 自動跑測試，測試通過後自動部署到 GitHub Pages。

## Pipeline 流程

```
git push
    │
    ▼
[CI] Run Tests (pytest)
    │  pass
    ▼
[CD] Freeze Flask → 靜態 HTML → Deploy to GitHub Pages
```

## 本地執行

```bash
pip install -r requirements.txt

# 啟動 dev server
python app.py

# 跑測試
pytest tests/ -v

# 產生靜態檔
python freeze.py
```

## 專案結構

```
├── app.py                    # Flask app（/, /health, /items）
├── freeze.py                 # 將 Flask 凍結成靜態 HTML
├── requirements.txt
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py           # 4 個 pytest 測試
└── .github/
    └── workflows/
        └── ci-cd.yml         # GitHub Actions pipeline
```
