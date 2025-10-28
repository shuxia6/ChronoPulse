import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from config.language import LANG
import calendar
from config.settings import MOOD_SCORES
import numpy as np
from data.handlers import load_data

def plot_daily_trend(date_str, lang="zh"):
    """
    绘制某一天的心情趋势
    :param date_str: 指定日期，格式 "YYYY-MM-DD"
    :param lang: 语言（"zh" 或 "en"）
    """
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    lang_dict = {
        "zh": {
            "title": f"{date_str} {LANG['zh']['plot_title']}",
            "xlabel": LANG['zh']['plot_xlabel'],
            "ylabel": LANG['zh']['plot_ylabel'],
            "no_data": f"没有找到 {date_str} 的记录。"
        },
        "en": {
            "title": f"Mood Trend on {date_str}",
            "xlabel": LANG['en']['plot_xlabel'],
            "ylabel": LANG['en']['plot_ylabel'],
            "no_data": f"No records found for {date_str}."
        }
    }

    # 使用常量生成映射
    mood_score = MOOD_SCORES
    # 动态生成 mood_label（基于分数反向映射）
    zh_moods = {v: k for k, v in MOOD_SCORES.items() if k in ["开心", "一般", "压力大"]}
    en_moods = {v: k for k, v in MOOD_SCORES.items() if k in ["Happy", "Neutral", "Stressed"]}
    mood_label = {"zh": zh_moods, "en": en_moods}
    # 动态生成 color_map（基于心情键）
    color_map = {
        "开心": "#2ca02c", "一般": "#ff7f0e", "压力大": "#d62728",
        "Happy": "#2ca02c", "Neutral": "#ff7f0e", "Stressed": "#d62728"
    }

    data = load_data()
    daily_records = [row for row in data if row["datetime"].startswith(date_str)]

    if not daily_records:
        print(lang_dict[lang]["no_data"])
        return

    times = [row["datetime"].split(" ")[1] for row in daily_records]
    scores = [mood_score[row["mood"]] for row in daily_records]
    moods = [row["mood"] for row in daily_records]

    plt.figure(figsize=(10, 5))
    for i, (time, score, mood) in enumerate(zip(times, scores, moods)):
        plt.plot(time, score, marker="o", color=color_map[mood], markersize=8)

    plt.plot(times, scores, linestyle="-", color="#1f77b4", alpha=0.7, label=LANG[lang]["plot_ylabel"])

    if scores:
        max_idx = scores.index(max(scores))
        min_idx = scores.index(min(scores))

        plt.annotate(LANG[lang]["plot_best"].format(mood_label[lang][scores[max_idx]]),
                     xy=(times[max_idx], scores[max_idx]), xytext=(0, 15),
                     textcoords="offset points", ha='center', color="#2ca02c",
                     arrowprops=dict(arrowstyle="->", color="#2ca02c"))

        plt.annotate(LANG[lang]["plot_worst"].format(mood_label[lang][scores[min_idx]]),
                     xy=(times[min_idx], scores[min_idx]), xytext=(0, -25),
                     textcoords="offset points", ha='center', color="#d62728",
                     arrowprops=dict(arrowstyle="->", color="#d62728"))

    plt.title(lang_dict[lang]["title"], fontsize=14, pad=15)
    plt.xlabel(lang_dict[lang]["xlabel"], fontsize=12)
    plt.ylabel(lang_dict[lang]["ylabel"], fontsize=12)
    plt.ylim(0.5, 3.5)
    if len(times) > 5:
        plt.xticks(ticks=range(0, len(times), 2), labels=[times[i] for i in range(0, len(times), 2)], rotation=45,
                   fontsize=10)
    else:
        plt.xticks(rotation=45, fontsize=10)
    plt.legend()
    plt.tight_layout()

    output_file = f"mood_trend_{date_str}_{lang}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"图表已保存为 {output_file}")
    plt.show()


def plot_mood_calendar(year_month, lang="zh"):
    """
    绘制指定月份的心情日历
    :param year_month: 年月，格式 "YYYY-MM"
    :param lang: 语言（"zh" 或 "en"）
    """
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    lang_dict = {
        "zh": {
            "title": f"{year_month} 心情日历",
            "no_data": f"没有找到 {year_month} 的记录。",
            "xlabel": "周",
            "ylabel": "星期",
            "days": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        },
        "en": {
            "title": f"Mood Calendar for {year_month}",
            "no_data": f"No records found for {year_month}.",
            "xlabel": "Week",
            "ylabel": "Day",
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        }
    }

    # 使用常量生成映射
    mood_score = MOOD_SCORES
    # 动态生成 mood_label
    zh_moods = {v: k for k, v in MOOD_SCORES.items() if k in ["开心", "一般", "压力大"]}
    en_moods = {v: k for k, v in MOOD_SCORES.items() if k in ["Happy", "Neutral", "Stressed"]}
    mood_label = {"zh": zh_moods, "en": en_moods}
    # color_map 保持基于分数
    color_map = {3: "#2ca02c", 2: "#ff7f0e", 1: "#d62728"}

    # 解析年月
    try:
        year, month = map(int, year_month.split("-"))
        cal = calendar.monthcalendar(year, month)
    except ValueError:
        print("请输入有效年月 (格式 YYYY-MM) / Please enter a valid year-month (format YYYY-MM)")
        return

    data = load_data()
    month_records = [row for row in data if row["datetime"].startswith(year_month)]

    if not month_records:
        print(lang_dict[lang]["no_data"])
        return

    # 计算每天的平均心情分数
    daily_scores = {}
    for row in month_records:
        date = row["datetime"].split(" ")[0]
        if date not in daily_scores:
            daily_scores[date] = []
        try:
            daily_scores[date].append(mood_score[row["mood"]])
        except KeyError:
            print(f"警告: 在 {date} 发现未知心情 '{row['mood']}'，已跳过。")

    # 平均分数并映射到颜色
    day_colors = {}
    day_labels = {}
    for date, scores in daily_scores.items():
        if not scores: continue  # 跳过空列表
        avg_score = sum(scores) / len(scores)
        rounded_score = round(avg_score)  # 取整到最近的心情分数
        day_colors[date] = color_map.get(rounded_score, "#d3d3d3")  # 灰色为默认
        # 确保 rounded_score 在 mood_label 中
        if rounded_score not in mood_label[lang]:
            rounded_score = 2  # 默认为“一般”

        day_labels[date] = f"{date.split('-')[-1]}: {mood_label[lang][rounded_score]} ({avg_score:.1f})"  # 简化标签

    # 绘制日历
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.set_aspect("equal")

    # 设置日历网格
    for week, days in enumerate(cal):
        for day_idx, day in enumerate(days):
            if day != 0:  # 非空日期
                date_str = f"{year}-{month:02d}-{day:02d}"
                color = day_colors.get(date_str, "#f0f0f0")  # 默认浅灰色
                ax.add_patch(plt.Rectangle((week, 6 - day_idx), 1, 1, facecolor=color, edgecolor="black"))

                if date_str in day_labels:
                    avg_val = float(day_labels[date_str].split('(')[-1].replace(')', ''))
                    ax.text(week + 0.5, 6 - day_idx + 0.5, f"{day}\n({avg_val:.1f})", ha="center", va="center",
                            fontsize=9, color="black", linespacing=1.5)
                else:
                    ax.text(week + 0.5, 6 - day_idx + 0.5, str(day), ha="center", va="center", fontsize=10,
                            color="black")

    # 设置标题和轴标签
    plt.title(lang_dict[lang]["title"], fontsize=14, pad=15)
    plt.xlabel(lang_dict[lang]["xlabel"], fontsize=12)
    plt.ylabel(lang_dict[lang]["ylabel"], fontsize=12)
    plt.xticks(np.arange(len(cal)) + 0.5, [f"Week {i + 1}" for i in range(len(cal))])  # 居中
    plt.yticks(np.arange(7) + 0.5, lang_dict[lang]["days"][::-1])  # 居中
    plt.xlim(0, len(cal))
    plt.ylim(0, 7)
    plt.gca().set_xticks(np.arange(len(cal) + 1), minor=True)
    plt.gca().set_yticks(np.arange(8), minor=True)
    plt.grid(which='minor', color='black', linestyle='-', linewidth=1)
    ax.tick_params(axis='both', which='minor', bottom=False, left=False)  # 隐藏 minor ticks

    plt.tight_layout()

    # 保存日历为 PNG
    output_file = f"mood_calendar_{year_month}_{lang}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"{LANG[lang]['calendar_saved']} {output_file} / Calendar saved as {output_file}")
    plt.show()