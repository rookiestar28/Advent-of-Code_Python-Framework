# utils/solution_base.py (增強版)

from pathlib import Path
from typing import List

class SolutionBase:
    def __init__(self, args):
        """
        基礎 Solution 類別的建構函式。
        - 儲存傳入的 args，並定義所有相關路徑（包含年份）。
        """
        self.args = args
        # 使用 pathlib 建立穩健的路徑
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data" / str(self.args.year) / f"day{self.args.day:02d}"
        self.solution_file = self.base_dir / "solutions" / str(self.args.year) / f"day{self.args.day:02d}.py"

    def _read_file(self, file_path: Path, is_raw: bool = False) -> List[str]:
        """
        從指定的檔案路徑讀取內容的核心函式，包含錯誤處理。
        """
        if not file_path.exists():
            print(f"⚠️  警告：找不到檔案: {file_path}")
            return []
        try:
            with file_path.open('r', encoding='utf-8') as f:
                if is_raw:
                    # is_raw=True，只移除換行符
                    return [line.rstrip('\n') for line in f.readlines()]
                else:
                    # is_raw=False，移除所有頭尾空白
                    return [line.strip() for line in f.readlines()]
        except IOError as e:
            print(f"❌ 錯誤：讀取檔案時發生錯誤 {file_path} - {e}")
            return []

    def get_puzzle_input(self) -> List[str]:
        """讀取真實的謎題輸入檔案。"""
        return self._read_file(self.data_dir / "puzzle_input.txt", self.args.raw)

    def get_test_inputs(self) -> List[List[str]]:
        """
        讀取所有 test_X_input.txt 檔案，回傳一個二維列表。
        例如：[ ['test1_line1', 'test1_line2'], ['test2_line1'] ]
        """
        test_inputs = []
        # 使用 pathlib 的 glob 功能尋找所有匹配的測試檔案
        for test_file in sorted(self.data_dir.glob("test_*_input.txt")):
            test_inputs.append(self._read_file(test_file, self.args.raw))
        return test_inputs

    def get_test_results(self, part_num: int) -> List[List[str]]:
        """
        讀取對應 Part 的所有 test_X_partY_result.txt 檔案。
        """
        test_results = []
        for result_file in sorted(self.data_dir.glob(f"test_*_part{part_num}_result.txt")):
            test_results.append(self._read_file(result_file))
        return test_results

    def solve(self, part_num: int):
        """
        主解題入口函式，由 app.py 呼叫。
        它會自動讀取輸入資料，並根據 part_num 呼叫對應的 part1 或 part2 方法。
        """
        data = self.get_puzzle_input()
        if not data:
            print("❌ 錯誤：無法讀取謎題輸入，終止執行。")
            return None

        if part_num == 1:
            return self.part1(data)
        elif part_num == 2:
            return self.part2(data)
        else:
            return None

    def part1(self, data: List[str]):
        raise NotImplementedError("Part 1 method not implemented.")

    def part2(self, data: List[str]):
        raise NotImplementedError("Part 2 method not implemented.")