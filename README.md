# Advent of Code - Python Automated Solver Framework

This is a highly automated and scalable solver framework for [Advent of Code (AoC)](https://adventofcode.com/), developed in Python 3. It aims to simplify all repetitive tasks (e.g., creating files, downloading inputs, submitting answers), allowing developers to focus 100% on the core fun of solving puzzles.

---

## ✨ Features

* **🚀 Fully Automated Workflow**: From daily file scaffolding and personal puzzle input downloads to answer submissions, the entire process can be handled with a single command line instruction.
* **🗓️ Multi-Year Support**: With the `--year` parameter, you can easily use this framework to tackle or practice AoC puzzles from any year (2015-present).
* **🏗️ Scalable Architecture**: Based on a `SolutionBase` inheritance design, when adding a new daily solution, you only need to focus on the core `part1` and `part2` algorithm logic.
* **🛡️ Robust Design**:
    * Securely manages your Session Cookie using a `.env` file.
    * Fully utilizes modern libraries like `requests` and `pathlib`.
    * Provides comprehensive error handling for all file and network operations.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/YourUsername/advent-of-code-framework.git
    cd advent-of-code-framework
    ```

2. **Create a Virtual Environment and Install Dependencies**:
    ```bash
    # Create virtual environment
    python -m venv venv
    # Activate virtual environment (Windows)
    .\venv\Scripts\activate
    # Activate virtual environment (macOS/Linux)
    # source venv/bin/activate

    # Install necessary libraries
    pip install -r requirements.txt
    ```

3. **Configure Session Cookie**:
    This step is required for automatic downloading and submission.
    * In the project root directory, create a file named `.env`.
    * Add the following content to the `.env` file, replacing the value after the equals sign with your own cookie:
        ```
        AOC_SESSION_COOKIE=53616c7465645f5f...[paste your long cookie string from the browser here]
        ```
    * You can find the `session` cookie in your browser's developer tools after logging into the AoC website.

---

## 🕹️ Usage

All operations are performed via the `app.py` script.

#### 1. Create Daily Challenge Structure

When you want to start a new day's challenge (e.g., Day 5 of 2024), run this command:

```bash
python app.py --year 2024 -d 5 --add
```

This command will automatically create `solutions/day05.py` and download your personal puzzle input to `data/day05/puzzle_input.txt`.

#### 2. Run Your Solution

After writing your part1 code in `solutions/day05.py`, run the following command to calculate the answer:

```bash
python app.py -y 2024 -d 5 -p 1
```

**Tip**: If the `-y` parameter is not provided, the year defaults to the current year.

#### 3. Submit Your Answer Automatically

Once you have the correct answer, add the `--submit` flag to submit it automatically:

```bash
python app.py -y 2024 -d 5 -p 1 --submit
```

#### 4. Full List of Options

```
usage: app.py [-h] [-y year] [-d day_number] [-p part_number] [--raw] [--add] [--add-test-file test_number] [--skip-test] [--submit]

Advent of Code - Python Automated Solver Framework

options:
  -h, --help            show this help message and exit
  -y year, --year year  Optional, AoC event year (default: 2025)
  -d day_number, --day day_number
                        Required, day number of the AoC event (default: 6)
  -p part_number, --part part_number
                        Required, part number of the day of the AoC event (default: 1)
  --raw                 Optional, use raw input instead of stripped input
  --add                 Optional, create daily file structure
  --add-test-file test_number
                        Optional, create additional test files
  --skip-test           Optional, skipping tests
  --submit              Optional, submit your answer to AoC
```

---



# Advent of Code - Python 自動化解題框架

這是一個使用 Python 3 開發的、高度自動化且可擴展的 Advent of Code (AoC) 解題框架。它旨在簡化所有重複性的任務（如建立檔案、下載輸入、提交答案），讓開發者可以 100% 專注於解決謎題的核心樂趣。

## ✨ 功能特性

* **🚀 全自動化流程**: 從建立每日檔案、下載個人謎題輸入到提交答案，全程可由命令列一鍵完成。
* **🗓️ 支援多年份**: 透過 `--year` 參數，您可以輕鬆地使用此框架來挑戰或練習任何一年 (2015-至今) 的 AoC 題目。
* **🏗️ 可擴展的架構**: 基於 `SolutionBase` 的繼承設計，新增每日的解題方案時，您只需專注於核心的 `part1` 和 `part2` 演算法邏輯。
* **🛡️ 穩健的設計**:
    * 使用 `.env` 檔案安全地管理您的 Session Cookie。
    * 全面採用現代化的 `requests` 和 `pathlib` 函式庫。
    * 為所有檔案和網路操作提供完整的錯誤處理。

## ✨ 安裝與使用方式

* **請參照以上英文說明 

---

## 📝 License

This project is licensed under the MIT License.

---