# utils/submission.py

import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path

# --- 與 files.py 保持一致的現代化設定 ---
# 載入 .env 檔案中的環境變數
try:
    BASE_DIR = Path(__file__).resolve().parent.parent
except NameError:
    BASE_DIR = Path(".").resolve()

load_dotenv(BASE_DIR / ".env")

# 從環境變數讀取必要的設定
AOC_SESSION_COOKIE = os.getenv("AOC_SESSION_COOKIE")
# 使用我們在 files.py 中定義的、更穩健的 User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

class Submission:
    """
    一個用於向 Advent of Code 網站提交答案的工具類。
    """
    @staticmethod
    def send_answer(year: int, day: int, part: int, answer: str) -> None:
        """
        提交答案到 Advent of Code 網站。
        - 使用 requests 函式庫發送 POST 請求。
        - 採用更穩健的方式解析伺服器回應。
        - 函式簽名已更新，可接收 4 個參數。
        """
        if not AOC_SESSION_COOKIE:
            print("❌ 錯誤：無法提交答案，找不到 AOC_SESSION_COOKIE，請檢查 .env 檔案。", file=sys.stderr)
            return

        # 1. 修正函式簽名，並使用傳入的 year 參數
        url = f"https://adventofcode.com/{year}/day/{day}/answer"
        
        headers = {"User-Agent": USER_AGENT}
        cookies = {"session": AOC_SESSION_COOKIE}
        payload = {"level": part, "answer": str(answer)} # 確保答案是字串格式

        try:
            print("🚀 正在提交答案...")
            response = requests.post(url, headers=headers, cookies=cookies, data=payload, timeout=15)
            response.raise_for_status() # 檢查網路請求是否成功

            # 2. 簡化回應解析：直接檢查關鍵字，而不是用複雜的 regex
            content = response.text
            if "That's the right answer!" in content:
                print("\n✅ 恭喜！答案正確！您獲得了一顆金星 ⭐")
            elif "That's not the right answer." in content:
                if "your answer is too high" in content:
                    print("\n❌ 答案不正確。提示：您的答案太大了。")
                elif "your answer is too low" in content:
                    print("\n❌ 答案不正確。提示：您的答案太小了。")
                else:
                    print("\n❌ 答案不正確，請再試一次。")
            elif "You gave an answer too recently" in content:
                print("\n⏱️ 提交過於頻繁，請稍後再試。")
            elif "You don't seem to be solving the right level." in content:
                print("\n⚠️  您可能已經解決了這個部分，或者提交到了錯誤的部分。")
            else:
                # 如果是未知的回應，印出一些原始碼供除錯
                print("\n🤔 收到未知的伺服器回應，請手動前往網站確認。")
                
        except requests.exceptions.HTTPError as e:
             print(f"\n❌ 錯誤：提交失敗，伺服器回傳錯誤狀態碼 {e.response.status_code}。", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 錯誤：提交答案時網路連線失敗 - {e}", file=sys.stderr)