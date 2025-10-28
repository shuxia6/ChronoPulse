import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from data.handlers import load_data
from config.language import LANG
from config.settings import MOOD_SCORES

def generate_weekly_report(lang):
    """生成每周心情报告并绘制心情分布饼图"""
    # 设置 Seaborn 风格，与其他图表一致
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    data = load_data()
    if not data:
        print(LANG[lang]["no_data"])
        return

    # 获取最近7天的数据
    week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    recent_data = [
        row for row in data
        if datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M") >= week_ago
    ]

    if not recent_data:
        print(LANG[lang]["no_records_week"])
        return

    mood_score = MOOD_SCORES

    scores = []
    for row in recent_data:
        if row["mood"] in mood_score:
            scores.append(mood_score[row["mood"]])
        else:
            print(f"警告: 发现未知心情 '{row['mood']}'，已跳过。")

    if not scores:
        print(LANG[lang]["no_records_week"])
        return

    avg_score = sum(scores) / len(scores)

    # 统计心情分布
    mood_counts = {"开心/Happy": 0, "一般/Neutral": 0, "压力大/Stressed": 0}
    for row in recent_data:
        mood_key = "开心/Happy" if row["mood"] in ["开心", "Happy"] else \
            "一般/Neutral" if row["mood"] in ["一般", "Neutral"] else \
                "压力大/Stressed" if row["mood"] in ["压力大", "Stressed"] else None
        if mood_key:
            mood_counts[mood_key] += 1

    # 过滤掉计数为 0 的心情，避免饼图空标签
    labels = [key for key, count in mood_counts.items() if count > 0]
    counts = [count for count in mood_counts.values() if count > 0]

    color_map = {"开心/Happy": "#2ca02c", "一般/Neutral": "#ff7f0e", "压力大/Stressed": "#d62728"}
    colors = [color_map[label] for label in labels]

    if counts:  # 确保有数据才绘制
        plt.figure(figsize=(8, 8))

        explode = [0] * len(counts)
        if len(counts) > 1:
            min_idx = counts.index(min(counts))
            explode[min_idx] = 0.05  # 稍微拉出最小的块

        plt.pie(counts, labels=labels, colors=colors,
                autopct="%1.1f%%", startangle=90, textprops={"fontsize": 12},
                explode=explode, pctdistance=0.85)

        plt.title(LANG[lang]["weekly_report"].replace("===", "").strip() + " - 心情分布/Mood Distribution", fontsize=14)

        # 保存饼图为 PNG
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        output_file = f"weekly_mood_distribution_{timestamp}_{lang}.png"
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"{LANG[lang]['pie_chart_saved']} {output_file} / Pie chart saved as {output_file}")
        plt.show()

    # 打印文本报告
    print(f"\n{LANG[lang]['weekly_report']}")
    print(LANG[lang]["record_count"].format(len(recent_data)))
    print(LANG[lang]["avg_mood_score"].format(avg_score))

    # 按天分组
    daily_data = {}
    for row in recent_data:
        if row["mood"] not in mood_score: continue  # 跳过未知心情
        date = row["datetime"].split(" ")[0]
        if date not in daily_data:
            daily_data[date] = []
        daily_data[date].append(mood_score[row["mood"]])

    # 打印每日平均
    print(f"\n{LANG[lang]['daily_avg_mood']}")
    for date, scores in daily_data.items():
        if scores:
            print(f"{date}: {sum(scores) / len(scores):.2f}")

    # G给建议
    if avg_score >= 2.5:
        print(f"\n{LANG[lang]['week_summary_good']}")
    elif avg_score >= 1.5:
        print(f"\n{LANG[lang]['week_summary_normal']}")
    else:
        print(f"\n{LANG[lang]['week_summary_bad']}")

def export_daily_report(date_str, lang="zh"):
    """导出日报到文本文件"""
    mood_score = MOOD_SCORES

    data = load_data()
    daily_records = [row for row in data if row["datetime"].startswith(date_str)]

    if not daily_records:
        print(f"没有找到 {date_str} 的记录")
        return

    filename = f"mood_report_{date_str}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        # 根据语言切换报告标题
        if lang == "zh":
            f.write(f"心情日报 - {date_str}\n")
            f.write("=" * 30 + "\n\n")
            avg_text = "平均心情分数"
            summary_text = "总结"
            good_day = "今天是美好的一天! 🌞\n"
            ok_day = "今天过得还不错 🌱\n"
            bad_day = "今天可能有些困难，明天会更好! 💪\n"
        else:
            f.write(f"Daily Mood Report - {date_str}\n")
            f.write("=" * 30 + "\n\n")
            avg_text = "Average Mood Score"
            summary_text = "Summary"
            good_day = "Today was a good day! 🌞\n"
            ok_day = "Today was okay. 🌱\n"
            bad_day = "Today might have been tough, tomorrow is a new day! 💪\n"


        for record in daily_records:
            time = record["datetime"].split(" ")[1]
            try:
                # 备注信息也加入报告
                note = record.get("note", "")
                note_text = f" ({LANG[lang]['note_label']}: {note})" if note else ""
                f.write(f"{time}: {record['mood']} ({LANG[lang]['score_label']}: {mood_score[record['mood']]}){note_text}\n")
            except KeyError:
                f.write(f"{time}: {record['mood']} ({LANG[lang]['score_label']}: N/A){note_text}\n")

        scores = [mood_score[r["mood"]] for r in daily_records if r["mood"] in mood_score]
        if not scores:
            avg_score = 0
        else:
            avg_score = sum(scores) / len(scores)

        f.write(f"\n{avg_text}: {avg_score:.2f}\n")

        if avg_score >= 2.5:
            f.write(f"{summary_text}: {good_day}")
        elif avg_score >= 1.5:
            f.write(f"{summary_text}: {ok_day}")
        else:
            f.write(f"{summary_text}: {bad_day}")
    print(f"{LANG[lang]['report_saved']} {filename} / Report exported to {filename}")