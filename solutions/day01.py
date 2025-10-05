# solutions/day01.py

from utils.solution_base import SolutionBase

class Solution(SolutionBase):
    """
    繼承自 SolutionBase，專注於 Day 01 的核心解題邏輯。
    """
    def part1(self, data: list[str]) -> int:
        """
        解決 Part 1 問題。
        'data' 參數是由 SolutionBase 自動讀取並傳入的輸入檔案內容列表。
        """
        # 使用您原本的、能夠正確處理 "數字 空格 數字" 格式的程式碼
        # 這可以處理每行兩個由任意數量空格分隔的數字
        try:
            _left, _right = zip(*[map(int, line.split()) for line in data if line])
        except ValueError:
            print("❌ 錯誤：輸入檔案中包含無法處理的行，請檢查檔案格式是否為每行兩個數字。")
            return -1 # 回傳一個錯誤碼

        # 您的核心演算法邏輯
        distance = sum(abs(x - y) for x, y in zip(sorted(_left), sorted(_right)))
        return distance

    def part2(self, data: list[str]) -> int:
        """
        解決 Part 2 問題。
        """
        # 同樣，使用能正確處理輸入格式的程式碼
        try:
            _left, _right = zip(*[map(int, line.split()) for line in data if line])
        except ValueError:
            print("❌ 錯誤：輸入檔案中包含無法處理的行，請檢查檔案格式是否為每行兩個數字。")
            return -1

        # Part 2 的核心演算法邏輯
        score = sum(x * _right.count(x) for x in _left)
        return score