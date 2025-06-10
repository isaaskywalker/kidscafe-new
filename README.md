# 인용 리트윗 스크래퍼 (quote_retweet_scraper)

## 개요
이 스크립트는 X(구 트위터) 게시물 URL을 입력받아, 해당 게시물을 인용(quote)한 트윗을 전부 수집하고,
인용 리트윗을 한 사용자의 아이디(username)와 해당 트윗 작성 날짜를 `YYYY-MM-DD` 형식으로 정리합니다.

## 설치 및 준비
1. Python 3.8 이상이 설치되어 있어야 합니다.
2. 가상환경(venv)을 생성하는 것을 권장합니다.
    ```bash
    python3 -m venv venv
    source venv/bin/activate        # Linux/macOS
    venv\Scripts\activate.bat       # Windows
    ```
3. 의존 라이브러리 설치
    ```bash
    pip3 install -r requirements.txt
    ```

## 사용법
```bash
python3 quote_retweet_scraper.py "X_게시물_URL" [--max 최대_개수] [--delay 지연_초] [--output 출력_파일.json]
