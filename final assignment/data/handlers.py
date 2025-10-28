import csv
import os
import datetime
from utils.decorators import safe_file_operation
from config.settings import DATA_FILE, BACKUP_FILE
from config.settings import VALID_MOODS

@safe_file_operation
def backup_data():
    """创建数据备份"""
    if os.path.exists(DATA_FILE):
        import shutil
        shutil.copy2(DATA_FILE, BACKUP_FILE)
        return True
    return False

def load_data():
    """读取历史心情数据，并验证数据格式"""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print("警告: 数据文件不存在或为空 / Warning: Data file does not exist or is empty")
        return []

    # 使用常量
    valid_moods = VALID_MOODS
    data = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if not fieldnames or "datetime" not in fieldnames or "mood" not in fieldnames:
            print("错误: CSV 文件缺少必要的标题行 / Error: CSV file missing required headers")
            return []
        has_note = "note" in fieldnames
        try:
            for row_num, row in enumerate(reader, start=2):  # 从第2行开始（跳过标题）
                try:
                    # 验证行完整性
                    if len(row) < 2:  # 至少需要 datetime 和 mood
                        print(f"警告: 第 {row_num} 行数据不完整: {row}")
                        continue
                    datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M")
                    if row["mood"] not in valid_moods:
                        print(f"警告: 跳过无效心情值 (第 {row_num} 行): {row['datetime']}, {row['mood']}")
                        continue
                    if not has_note:
                        row["note"] = ""
                    else:
                        # 清理备注中的换行符和多余空格
                        raw_note = row.get("note", "")
                        row["note"] = raw_note.replace('\n', ' ').replace('\r', ' ').strip()
                    data.append(row)
                except ValueError:
                    print(f"警告: 跳过无效时间格式 (第 {row_num} 行): {row.get('datetime', '未知')}")
                except KeyError as e:
                    print(f"错误: 第 {row_num} 行数据缺失字段 {e}: {row}")
        except csv.Error as e:
            print(f"CSV 文件解析错误: {e}")
            return []
    return data

@safe_file_operation
def save_mood_record(timestamp, mood_text, note=""):
    """保存心情记录到文件，包含备注"""
    if mood_text not in VALID_MOODS:
        print(f"错误: 无效的心情值 {mood_text}")
        return False

    try:
        datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    except ValueError:
        print(f"错误: 无效的时间戳格式 {timestamp}")
        return False

    # 清理备注中的换行符，替换为空格，避免CSV行混乱
    clean_note = note.replace('\n', ' ').replace('\r', ' ').strip()

    new_file = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["datetime", "mood", "note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if new_file:
            writer.writeheader()
        writer.writerow({"datetime": timestamp, "mood": mood_text, "note": clean_note})
    backup_data()
    return True

@safe_file_operation
def delete_last_record():
    """删除最后一条记录"""
    data = load_data()
    if data:
        removed = data.pop()
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["datetime", "mood", "note"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow({"datetime": row["datetime"], "mood": row["mood"], "note": row.get("note", "")})
        return removed
    return None