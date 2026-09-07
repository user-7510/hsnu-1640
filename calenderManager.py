import csv
import os
import sys
from datetime import date

csvPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calender.csv")
fieldNames = ["date", "subject", "range"]


def parseDateInput(text, today):
    text = text.strip()
    parts = text.split("/")
    if len(parts) == 3:
        y, m, d = parts
        y = int(y)
    elif len(parts) == 2:
        m, d = parts
        y = today.year
    elif len(parts) == 1:
        d = parts[0]
        m = today.month
        y = today.year
    else:
        raise ValueError(f"無法解析日期：{text}")
    return date(y, int(m), int(d))


def loadRows():
    if not os.path.exists(csvPath):
        return []
    with open(csvPath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def saveRows(rows):
    rows.sort(key=lambda r: r["date"])
    with open(csvPath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(rows)


def dropPastRows(rows, today):
    todayStr = today.isoformat()
    kept = [r for r in rows if r["date"] >= todayStr]
    removedCount = len(rows) - len(kept)
    return kept, removedCount


def printRows(rows):
    if not rows:
        print("目前沒有任何考程")
        return
    for i, r in enumerate(rows, start=1):
        print(f"{i}. {r['date']}  {r['subject']}  {r['range']}")


def addRow(rows, today):
    dateText = input("日期 (yyyy/mm/dd、mm/dd 或 dd)：")
    try:
        parsedDate = parseDateInput(dateText, today)
    except ValueError as e:
        print(f"日期格式錯誤：{e}")
        return
    subject = input("科目：").strip()
    examRange = input("範圍：").strip()
    rows.append({
        "date": parsedDate.isoformat(),
        "subject": subject,
        "range": examRange,
    })
    print("已新增")


def editRow(rows, today):
    printRows(rows)
    if not rows:
        return
    indexText = input("要修改第幾筆？（輸入編號）：").strip()
    if not indexText.isdigit() or not (1 <= int(indexText) <= len(rows)):
        print("編號錯誤")
        return
    target = rows[int(indexText) - 1]

    dateText = input(f"日期 [{target['date']}]（直接按 Enter 保留）：").strip()
    if dateText:
        try:
            target["date"] = parseDateInput(dateText, today).isoformat()
        except ValueError as e:
            print(f"日期格式錯誤：{e}")
            return

    subjectText = input(f"科目 [{target['subject']}]（直接按 Enter 保留）：").strip()
    if subjectText:
        target["subject"] = subjectText

    rangeText = input(f"範圍 [{target['range']}]（直接按 Enter 保留）：").strip()
    if rangeText:
        target["range"] = rangeText

    print("已更新")


def deleteRow(rows):
    printRows(rows)
    if not rows:
        return
    indexText = input("要刪除第幾筆？（輸入編號）：").strip()
    if not indexText.isdigit() or not (1 <= int(indexText) <= len(rows)):
        print("編號錯誤")
        return
    removed = rows.pop(int(indexText) - 1)
    print(f"已刪除：{removed['date']} {removed['subject']}")


def main():
    today = date.today()
    rows = loadRows()
    rows, removedCount = dropPastRows(rows, today)
    if removedCount:
        print(f"已自動移除 {removedCount} 筆過期考程")

    menu = """
1. 列出所有考程
2. 新增考程
3. 修改考程
4. 刪除考程
5. 儲存並離開
6. 不儲存離開
"""
    while True:
        print(menu)
        choice = input("請選擇：").strip()
        if choice == "1":
            printRows(rows)
        elif choice == "2":
            addRow(rows, today)
        elif choice == "3":
            editRow(rows, today)
        elif choice == "4":
            deleteRow(rows)
        elif choice == "5":
            saveRows(rows)
            print(f"已儲存至 {csvPath}")
            sys.exit(0)
        elif choice == "6":
            sys.exit(0)
        else:
            print("無效選項")


if __name__ == "__main__":
    main()

