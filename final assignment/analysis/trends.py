import datetime
from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from typing import List, Dict
from config.language import LANG
import seaborn as sns
from config.settings import MOOD_SCORES

def analyze_data(data: List[Dict], lang):
    """分析心情趋势（总览）"""
    if not data:
        return

    # 文本部分的统计分析保持不变，仍然基于所有记录
    scores = [MOOD_SCORES[row["mood"]] for row in data]
    dates = [datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M") for row in data]

    avg = sum(scores) / len(scores)
    best_moment = max(zip(dates, scores), key=lambda x: x[1])
    worst_moment = min(zip(dates, scores), key=lambda x: x[1])

    print(LANG[lang]["avg"].format(avg))
    # 这里的最佳/最差指的是具体时刻，作为趣味信息保留
    print(LANG[lang]["best_mood"].format(best_moment[0].strftime('%Y-%m-%d %H:%M'), best_moment[1]))
    print(LANG[lang]["worst_mood"].format(worst_moment[0].strftime('%Y-%m-%d %H:%M'), worst_moment[1]))

    latest_mood = data[-1]["mood"]
    give_suggestion(latest_mood, lang)

    # 绘制图表，现在会传入原始数据，由绘图函数自己处理聚合
    plot_daily_average_trend(data, lang)

def give_suggestion(mood, lang):
    """根据心情给出建议"""
    if mood in ["压力大", "Stressed"]:
        print(LANG[lang]["suggest_stress"])
    elif mood in ["一般", "Neutral"]:
        print(LANG[lang]["suggest_ok"])
    elif mood in ["开心", "Happy"]:
        print(LANG[lang]["suggest_happy"])


def plot_daily_average_trend(data: List[Dict], lang):
    """
    绘制每日平均心情趋势图。
    这个函数现在会聚合数据，只显示每天的平均值。
    """
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 按天聚合数据
    daily_scores = defaultdict(list)
    for row in data:
        date_key = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M").date()
        daily_scores[date_key].append(MOOD_SCORES[row["mood"]])

    if not daily_scores:
        return

    # 计算每天的平均分
    sorted_dates = sorted(daily_scores.keys())
    avg_scores = [sum(daily_scores[date]) / len(daily_scores[date]) for date in sorted_dates]

    plt.figure(figsize=(12, 6))

    # 绘制基础的折线图
    plt.plot(sorted_dates, avg_scores, linestyle='-', marker='o', color='#1f77b4',
             label=LANG[lang]["plot_ylabel"], zorder=1)

    # 绘制趋势线
    if len(sorted_dates) > 1:
        numeric_dates = [mdates.date2num(d) for d in sorted_dates]
        z = np.polyfit(numeric_dates, avg_scores, 1)
        p = np.poly1d(z)
        plt.plot(sorted_dates, p(numeric_dates), "r--", alpha=0.6, label=LANG[lang]["trend_line"], zorder=2)

    # --- 核心改动：用散点图高亮所有最高/最低点，并在图例中显示 ---
    if avg_scores:
        max_avg_score = max(avg_scores)
        min_avg_score = min(avg_scores)

        max_indices = [i for i, score in enumerate(avg_scores) if score == max_avg_score]
        min_indices = [i for i, score in enumerate(avg_scores) if score == min_avg_score]

        max_dates = [sorted_dates[i] for i in max_indices]
        max_scores_vals = [avg_scores[i] for i in max_indices]

        min_dates = [sorted_dates[i] for i in min_indices]
        min_scores_vals = [avg_scores[i] for i in min_indices]

        # 用散点图高亮所有最高点
        label_best = f"{LANG[lang]['plot_best']} ({max_avg_score:.1f})"
        plt.scatter(max_dates, max_scores_vals, s=150, facecolors='none', edgecolors='#2ca02c', linewidth=2,
                    label=label_best, zorder=3)

        # 用散点图高亮所有最低点
        label_worst = f"{LANG[lang]['plot_worst']} ({min_avg_score:.1f})"
        plt.scatter(min_dates, min_scores_vals, s=150, marker='x', color='#d62728', linewidth=2,
                    label=label_worst, zorder=3)

    # 设置图表样式
    plt.title(LANG[lang]["plot_title"], fontsize=14, pad=15)
    plt.xlabel(LANG[lang]["plot_xlabel"], fontsize=12)
    plt.ylabel(LANG[lang]["plot_ylabel"], fontsize=12)
    plt.ylim(0.5, 3.5)

    # 优化X轴日期显示
    ax = plt.gca()
    locator = mdates.AutoDateLocator(minticks=5, maxticks=12)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # 显示图例
    plt.legend(fontsize=10)
    plt.grid(True, which='major', linestyle='--', linewidth=0.5)
    plt.gcf().autofmt_xdate()

    output_file = f"mood_trend_daily_avg_{lang}.png"
    print(LANG[lang]["plot_saved"].format(output_file))
    plt.tight_layout()
    plt.show()