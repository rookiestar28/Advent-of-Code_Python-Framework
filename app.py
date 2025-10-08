import argparse
import importlib
import datetime
import sys
from typing import Optional

# 假設 submission 和 files 模組也已相應更新
from utils.submission import Submission
from utils.files import Files


def main() -> None:
    """
    Advent of Code 框架的主執行函式。
    負責解析命令列參數並調度相應的功能。
    """
    # --- 1. 最重要的修改：加入年份支援 ---
    current_year = datetime.date.today().year
    current_day = datetime.date.today().day

    parser = argparse.ArgumentParser(
        description="Advent of Code solution runner",
        formatter_class=argparse.RawTextHelpFormatter  # 改善 help 訊息的排版
    )
    # 新增 --year 參數，預設為當前年份
    parser.add_argument("-y", "--year", dest="year", default=current_year, metavar="year", type=int,
                        help=f"Optional, AoC event year (default: {current_year})")
    parser.add_argument("-d", "--day", dest="day", default=current_day, metavar="day_number", type=int,
                        help=f"Required, day number of the AoC event (default: {current_day})")
    parser.add_argument("-p", "--part", dest="part", default=1, metavar="part_number", type=int,
                        help="Required, part number of the day of the AoC event (default: 1)")
    parser.add_argument("--raw", action="store_true", help="Optional, use raw input instead of stripped input")
    parser.add_argument("--add", action="store_true", help="Optional, create daily file structure")
    parser.add_argument("--add-test-file", metavar="test_number", type=int,
                        help="Optional, create additional test files")
    parser.add_argument("--skip-test", action="store_true", help="Optional, skipping tests")
    parser.add_argument("--benchmark", action="store_true", help="Optional, benchmarking the code, and also skipping tests")
    parser.add_argument("--submit", action="store_true", help="Optional, submit your answer to AoC")
    args = parser.parse_args()

    # --- 2. 更新函式呼叫，傳入 year 參數 ---
    if not 0 < args.day < 26:
        print("❌ 錯誤：日期必須介於 1 到 25 之間。", file=sys.stderr)
        exit(1)
    elif args.add:
        Files.add_day(args.year, args.day)
    elif args.add_test_file is not None:
        Files.add_test_file(args.year, args.day, args.add_test_file) 
    elif args.part not in [1, 2]:
        print("❌ 錯誤：部分必須是 1 或 2。", file=sys.stderr)
        exit(1)
    else:
        # --- 3. 增加完整的錯誤處理 ---
        try:
            print(f"▶️  正在執行 {args.year} Day {args.day:02d} Part {args.part} 的解答...\n")
            
            # 動態載入對應的解題模組
            solution_module = importlib.import_module(f"solutions.{args.year}.day{args.day:02d}")
            
            # 將整個 args 物件傳遞過去，降低耦合度
            # 假設 Solution 的 __init__ 已修改為 def __init__(self, args):
            solution_instance = solution_module.Solution(args)

            answer: Optional[str] = solution_instance.solve(part_num=args.part)
            
            if answer is not None:
                print(f"✨ 解答是: {answer}\n")
            else:
                print("🤔 解答函式沒有回傳結果。\n")

            if answer and args.submit:
                print("🚀 正在提交答案...")
                # 假設 Submission.send_answer 也已更新
                Submission.send_answer(args.year, args.day, args.part, answer)

        except ImportError:
            print(f"❌ 錯誤：找不到解答檔案 'solutions/day{args.day:02d}.py'。", file=sys.stderr)
            print("   請先執行 --add 指令來建立檔案。", file=sys.stderr)
            exit(1)
        except AttributeError:
            print(f"❌ 錯誤：'solutions/day{args.day:02d}.py' 中缺少必要的 'Solution' 類別。", file=sys.stderr)
            exit(1)
        except Exception as e:
            print(f"💥 執行解答時發生未預期的錯誤: {e}", file=sys.stderr)
            # 可以在此處印出更詳細的 traceback 供除錯
            # import traceback
            # traceback.print_exc()
            exit(1)


if __name__ == "__main__":
    main()