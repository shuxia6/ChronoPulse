import datetime
import csv
import json
from data.handlers import load_data
from config.language import LANG
from utils.decorators import safe_file_operation
from config.settings import MOOD_SCORES

@safe_file_operation
def export_data(lang, format="csv"):
    """导出数据到 CSV 或 JSON 文件，包含心情分数"""
    data = load_data()
    if not data:
        print(LANG[lang]["no_data"])
        return

    # 使用常量
    mood_score = MOOD_SCORES

    # 生成导出文件名，带时间戳
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_file = f"mood_export_{timestamp}.{format}"

    if format == "csv":
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["datetime", "mood", "score"])  # 添加 score 列
            for row in data:
                score = mood_score.get(row["mood"], 2)
                writer.writerow([row["datetime"], row["mood"], score])
    elif format == "json":
        export_data = [
            {"datetime": row["datetime"], "mood": row["mood"], "score": mood_score.get(row["mood"], 2)}
            for row in data
        ]
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    else:
        print("无效的导出格式 / Invalid export format")
        return

    # 双语提示
    print(f"{LANG[lang]['export_data_success']} {output_file} / Data exported to {output_file}")