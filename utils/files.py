import os
import sys
import datetime
from pathlib import Path
from time import sleep

# --- 現代化的依賴管理 ---
# 確保您已經在 requirements.txt 中加入了 requests 和 python-dotenv
# 並執行了 pip install -r requirements.txt
import requests
from dotenv import load_dotenv

# --- 1. 設定管理與靈活性 ---
# 使用 pathlib 定義基礎路徑，不再依賴 get_path()
# 這假設 files.py 位於 "utils" 資料夾下，專案根目錄是上一層
try:
    BASE_DIR = Path(__file__).resolve().parent.parent
except NameError:
    # 如果在互動式環境中執行，__file__ 可能未定義
    BASE_DIR = Path(".").resolve()

# 從專案根目錄的 .env 檔案載入環境變數
load_dotenv(BASE_DIR / ".env")

# 將設定值定義為常數，方便管理
AOC_SESSION_COOKIE = os.getenv("AOC_SESSION_COOKIE")
SOLUTIONS_DIR = BASE_DIR / "solutions"
DATA_DIR = BASE_DIR / "data"  # 保持與原專案一致的 "data" 資料夾名稱
TEMPLATE_URL = "https://raw.githubusercontent.com/nitekat1124/aoc-tool/files/template-files/solutions/day_sample.py"
# 好的實踐：在 User-Agent 中提供聯繫方式，以便 AoC 管理員識別請求來源
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

class Files:
    """
    一個用於處理 Advent of Code 專案檔案操作的工具類。
    包含建立每日解題檔案、下載謎題輸入等功能。
    所有方法均為靜態方法。
    """

    @staticmethod
    def download_puzzle_input(year: int, day: int) -> str | None:
        """
        使用 requests 下載指定年份和日期的謎題輸入。
        包含完整的錯誤處理和設定檢查。

        Args:
            year (int): Advent of Code 的年份。
            day (int): 挑戰的日期。

        Returns:
            str | None: 成功時回傳謎題輸入內容，失敗時回傳 None。
        """
            # --- 請在這裡加入以下這行正確的除錯碼 ---
        print(f"--- DEBUG: 正在使用的 Cookie: \"{AOC_SESSION_COOKIE}\" ---")
        if not AOC_SESSION_COOKIE:
            print("❌ 錯誤：找不到 AOC_SESSION_COOKIE，請檢查專案根目錄的 .env 檔案。", file=sys.stderr)
            return None

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        headers = {"User-Agent": USER_AGENT}
        cookies = {"session": AOC_SESSION_COOKIE}

        try:
            print(f"📡 正在從 {url} 下載輸入...")
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            response.raise_for_status()  # 如果 HTTP 狀態碼不是 2xx，則拋出異常
            print("✅ 下載成功！")
            return response.text.strip()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ 錯誤：第 {day} 天的謎題輸入尚未開放或不存在。", file=sys.stderr)
            else:
                print(f"❌ 錯誤：請求失敗，狀態碼 {e.response.status_code}。很可能是 Session Cookie 已過期或無效。", file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 錯誤：網路連線失敗 - {e}", file=sys.stderr)
            return None

    @staticmethod
    def add_day(year: int, day: int) -> None:
        """
        為指定的日期建立完整的檔案結構，現在會包含年份目錄。
        """
        print(f"📁 正在為 {year} Day {day:02d} 建立檔案結構...")

        # --- 修改點：在路徑中加入 year ---
        year_solutions_dir = SOLUTIONS_DIR / str(year)
        year_data_dir = DATA_DIR / str(year)

        # --- 建立解決方案檔案 ---
        try:
            year_solutions_dir.mkdir(parents=True, exist_ok=True)
            solution_file = year_solutions_dir / f"day{day:02d}.py"
            if not solution_file.exists():
                print(f"📄 正在從遠端下載模板檔案...")
                response = requests.get(TEMPLATE_URL, timeout=10)
                response.raise_for_status()
                solution_file.write_text(response.text, encoding="utf-8")
                print(f"   已建立檔案: {solution_file}")
        except (requests.exceptions.RequestException, IOError) as e:
            print(f"❌ 錯誤：無法建立解決方案檔案 - {e}", file=sys.stderr)
            return

        # --- 建立資料夾和測試檔案 ---
        try:
            day_data_dir = year_data_dir / f"day{day:02d}"
            day_data_dir.mkdir(parents=True, exist_ok=True)

            files_to_create = [
                "puzzle_input.txt", "test_1_input.txt",
                "test_1_part1_result.txt", "test_1_part2_result.txt"
            ]
            for filename in files_to_create:
                file_path = day_data_dir / filename
                if not file_path.exists():
                    file_path.touch()
                    print(f"   已建立檔案: {file_path}")
        except IOError as e:
            print(f"❌ 錯誤：無法建立資料檔案 - {e}", file=sys.stderr)
            return

        # --- 下載並寫入謎題輸入 ---
        input_path = day_data_dir / "puzzle_input.txt"
        if input_path.stat().st_size == 0:
            # 檢查謎題是否已開放
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            # AoC 謎題在美國東部時間午夜開放 (UTC-5)
            release_time_utc = datetime.datetime(year, 12, day, 5, 0, 0, tzinfo=datetime.timezone.utc)

            if now_utc < release_time_utc:
                print(f"⏳ 謎題輸入將於 {release_time_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC 開放")
                while datetime.datetime.now(datetime.timezone.utc) < release_time_utc:
                    remaining = release_time_utc - datetime.datetime.now(datetime.timezone.utc)
                    # \r 讓游標回到行首，\033[K 清除該行內容
                    print(f"\r   倒數計時: {str(remaining).split('.')[0]}...", end="")
                    sleep(1)
                print("\n") # 倒數結束後換行

            puzzle_content = Files.download_puzzle_input(year, day)
            if puzzle_content:
                try:
                    input_path.write_text(puzzle_content, encoding="utf-8")
                    print(f"📥 已將謎題輸入儲存至: {input_path}")
                except IOError as e:
                    print(f"❌ 錯誤：無法寫入謎題輸入檔案 - {e}", file=sys.stderr)
        else:
            print("ℹ️  謎題輸入檔案已存在，跳過下載。")

    @staticmethod
    def add_test_file(year: int, day: int, test_no: int) -> None: # 新增 year 參數
        """
        為指定的日期建立額外的測試檔案，現在會包含年份目錄。
        """
        print(f"📝 正在為 {year} Day {day:02d} 新增第 {test_no} 組測試檔案...")
        try:
            # --- 修改點：在路徑中加入 year ---
            day_data_dir = DATA_DIR / str(year) / f"day{day:02d}"
            day_data_dir.mkdir(parents=True, exist_ok=True)

            files_to_create = [
                f"test_{test_no}_input.txt",
                f"test_{test_no}_part1_result.txt",
                f"test_{test_no}_part2_result.txt"
            ]
            for filename in files_to_create:
                file_path = day_data_dir / filename
                if not file_path.exists():
                    file_path.touch()
                    print(f"   已建立檔案: {file_path}")
                else:
                    print(f"   檔案已存在: {file_path}")
        except IOError as e:
            print(f"❌ 錯誤：無法建立測試檔案 - {e}", file=sys.stderr)