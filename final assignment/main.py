import datetime
from config.language import get_language, LANG, change_language
from data.handlers import backup_data, load_data, save_mood_record, delete_last_record
from analysis.reports import generate_weekly_report, export_daily_report
from analysis import daily_analysis
from analysis import trends
from config.settings import MOOD_MAP, VALID_MOODS

def record_mood(lang):
    """记录当前心情并保存到文件，包含备注"""
    # 根据当前语言，获取对应的心情选项映射
    mood_map = MOOD_MAP[lang]
    user_input = input(LANG[lang]["choose_mood"]).strip()

    # 如果用户没有输入任何内容，则直接返回
    if not user_input:
        print(LANG[lang]["invalid"])
        return lang

    mood_text = None

    # 尝试将用户的输入转换为整数
    try:
        mood_choice = int(user_input)
        # 检查输入的数字是否是有效选项 (1, 2, 3)
        if mood_choice in mood_map:
            mood_text = mood_map[mood_choice]
    except ValueError:
        # 如果用户输入的不是数字，则检查是否为有效的文本心情
        if user_input in VALID_MOODS:
            mood_text = user_input
        # (如果输入 "Happy"，mood_text 变为 "Happy")
        # (如果输入 "开心"，mood_text 变为 "开心")

    # 如果 mood_text 仍然是 None，说明输入无效
    if mood_text is None:
        print(LANG[lang]["invalid"])
        return lang

    # 获取当前时间，并格式化为 "年-月-日 时:分"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # 允许用户输入备注
    note = input(LANG[lang]["enter_note"]).strip()

    # 调用保存函数，如果保存成功，则打印确认信息
    if save_mood_record(timestamp, mood_text, note):
        # "note or LANG[lang]['no_note']" 是一个巧妙的用法：
        # 如果 note 不为空，就使用 note；如果 note 为空，就使用语言文件中的“无备注”文本
        print(
            f"{LANG[lang]['saved']}: {timestamp}, {mood_text}, {LANG[lang]['note_label']}: {note or LANG[lang]['no_note']}")
    return lang


def manage_data(lang):
    """数据管理功能，包括查看、删除、导出和搜索"""
    print(f"\n{LANG[lang]['data_management']}")
    print(LANG[lang]["view_records"])
    print(LANG[lang]["delete_record"])
    print(LANG[lang]["export_data"])
    print(LANG[lang]["search_notes"])
    choice = input(LANG[lang]["choose_option"]).strip()

    if choice == "1":
        data = load_data()
        if not data:
            print(LANG[lang]["no_data"])
            return
        print(f"加载了 {len(data)} 条记录 / Loaded {len(data)} records")
        # "data[-10:]" 是列表切片操作，表示只取列表的最后10个元素
        for i, row in enumerate(data[-10:]):
            # "row.get('note', ...)" 是一个安全的字典取值方法
            # 它会尝试获取 'note' 键的值，如果不存在，则返回后面提供的默认值
            note = row.get("note", LANG[lang]["no_note"])
            print(f"{i + 1}. {row['datetime']}: {row['mood']}, {LANG[lang]['note_label']}: {note}")

    elif choice == "2":
        removed = delete_last_record()
        if removed:
            note = removed.get("note", LANG[lang]["no_note"])
            print(LANG[lang]["record_deleted"].format(
                f"{removed['datetime']}, {removed['mood']}, {LANG[lang]['note_label']}: {note}"))
        else:
            print(LANG[lang]["no_data_to_delete"])

    elif choice == "3":
        print(LANG[lang]["choose_export_format"])
        format_choice = input(LANG[lang]["choose_option"]).strip()
        from utils.helpers import export_data  # 在需要时才导入，避免循环导入问题
        if format_choice == "1":
            export_data(lang, format="csv")
        elif format_choice == "2":
            export_data(lang, format="json")
        else:
            print(LANG[lang]["invalid_input"])

    elif choice == "4":
        keyword = input(LANG[lang]["enter_keyword"]).strip().lower()
        if not keyword:
            return  # 如果用户没输入关键词，则返回

        data = load_data()
        # 列表推导式：遍历所有数据，如果关键词在备注中（不区分大小写），则保留
        results = [row for row in data if keyword in row.get('note', '').lower()]

        if not results:
            print(LANG[lang]["no_keyword_found"].format(keyword))
        else:
            print(LANG[lang]["found_records_for"].format(len(results), keyword))
            for row in results:
                print(f"  - {row['datetime']}: {row['mood']} ({LANG[lang]['note_label']}: {row['note']})")

    else:
        print(LANG[lang]["invalid_input"])


def main():
    """程序的主入口函数"""
    # 从配置文件或默认设置中获取当前语言
    lang = get_language()
    print(LANG[lang]["welcome"])
    # 程序启动时，自动备份一次数据
    backup_data()
    # 主循环，让程序持续运行直到用户选择退出
    while True:
        print("\n" + "=" * 30)
        choice = input(LANG[lang]["menu"]).strip()

        if choice == "1":
            lang = record_mood(lang)

        elif choice == "2":
            # 获取今天的日期并格式化
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            # 调用更新后的函数（它现在内部使用健壮的加载器）
            daily_analysis.plot_daily_trend(today, lang=lang)

        elif choice == "3":
            generate_weekly_report(lang)

        elif choice == "4":
            manage_data(lang)

        elif choice == "5":
            # 这是一个内部循环，用于验证用户输入的年月格式是否正确
            while True:
                year_month = input(LANG[lang]["enter_year_month"]).strip()
                try:
                    # 尝试用指定的格式解析用户输入，如果成功，说明格式正确
                    datetime.datetime.strptime(year_month, "%Y-%m")
                    break  # 格式正确，跳出内部循环
                except ValueError:
                    # 如果解析失败，说明格式错误，提示用户并继续循环
                    print("格式错误，请输入 YYYY-MM 格式 / Invalid format, please use YYYY-MM.")
            # 调用更新后的函数
            daily_analysis.plot_mood_calendar(year_month, lang=lang)

        elif choice == "6":
            data = load_data()
            if not data:
                print(LANG[lang]["no_data"])
            else:
                trends.analyze_data(data, lang)

        elif choice == "7":
            # 内部循环，验证日期格式
            while True:
                date_str = input(LANG[lang]["enter_date"]).strip()
                try:
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    break  # 格式正确，跳出
                except ValueError:
                    print("格式错误，请输入 YYYY-MM-DD 格式 / Invalid format, please use YYYY-MM-DD.")
            export_daily_report(date_str, lang=lang)

        elif choice == "8":
            # 调用切换语言函数，并更新当前的语言设置
            lang = change_language()

        elif choice == "0":
            print(LANG[lang]["exit_message"])
            break  # 跳出主循环，结束程序
        else:
            print(LANG[lang]["invalid_input"])

if __name__ == "__main__":
    main()