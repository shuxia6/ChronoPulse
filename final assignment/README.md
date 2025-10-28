# ChronoPulse (时光脉搏) ⏱️❤️

`ChronoPulse` is a bilingual (EN/ZH) Mental Health Assistant built with Python. It is a lightweight command-line tool (CLI) designed to help users log, track, and analyze their daily emotional patterns.

`ChronoPulse` 是一个使用 Python 构建的双语（中/英）心理健康助手。它是一个轻量级的命令行工具（CLI），专为帮助用户记录、追踪和分析他们的日常情绪模式而设计。

It's more than just a diary; it's a powerful personal analytics tool that transforms abstract emotions into intuitive visualizations, helping users gain insights and understand themselves better.

它不仅仅是一个日记本，更是一个强大的个人数据分析工具，能将抽象的情绪转化为直观的可视化图表，帮助用户获得洞察并更好地理解自己。

## 🌟 Core Features / 核心功能

This tool provides all features through a simple menu system:
本工具通过一个简洁的菜单系统 提供所有功能：

### 1\. 📝 Mood Logging & Management / 情绪记录与管理

  * **Log Mood**: Quickly log your current mood (Happy, Neutral, Stressed).
      * **记录心情**: 快速记录当前的心情（开心, 一般, 压力大）。
  * **Add Notes**: Add detailed text notes to each entry.
      * **添加备注**: 为每条记录添加详细的文字备注。
  * **Data Management**:
      * **数据管理**:
      * View the last 10 records. / 查看最近 10 条记录。
      * Safely delete the last record. / 安全删除最后一条记录。
      * Search all historical notes by keyword. / 通过关键词搜索所有历史备注。

### 2\. 📊 Powerful Data Visualization / 强大的数据可视化

  * **📈 Daily Mood Trend**: View emotional fluctuations within a specific **day**, highlighting the best and worst moments.
      * **每日心情波动图**: 查看指定**一天**内的情绪起伏，高亮显示最佳和最差时刻。
  * **📅 Monthly Mood Calendar**: Display the average daily mood for a specific **month** as a heatmap, providing an at-a-glance overview.
      * **月度心情日历**: 以热力图的形式展示指定**一月**中每天的平均情绪，一目了然。
  * **📉 Overall Trend**: Analyze the average mood trend across **all** historical data and plot a fitted trend line.
      * **长期总趋势**: 分析**所有**历史数据的平均情绪走势，并绘制一条拟合的趋势线。
  * **📊 Weekly Report**: Generate a **pie chart** of mood distribution for the past 7 days, accompanied by a brief text summary.
      * **每周情绪分布**: 生成过去 7 天的情绪分布**饼图**，并附上一份简短的文本总结报告。

### 3\. 🌐 Bilingual Support / 双语支持

  * **Language Toggle**: Switch between Chinese (zh) and English (en) interfaces at any time.
      * **中英切换**: 可以在中文和英文界面之间随时切换。
  * **Localized Charts**: All generated chart titles and labels also change according to the language setting.
      * **图表本地化**: 所有生成的图表标题、标签也会随语言设置而改变。

### 4\. 🗃️ Data Export & Safety / 数据导出与安全

  * **Export Daily Report**: Export all records (including notes) for a specific day into a `.txt` file.
      * **导出日报**: 将指定某一天的所有记录（含备注）导出为 `.txt` 文本文件。
  * **Export Full Data**: Export all historical data as `CSV` or `JSON` for further analysis in Excel or other tools.
      * **导出全量数据**: 将所有历史数据导出为 `CSV` 或 `JSON` 格式，便于在 Excel 或其他工具中进一步分析。
  * **Auto-Backup**: Automatically creates a backup (`mood_log_backup.csv`) every time a new record is saved.
      * **自动备份**: 每次保存新记录时，都会自动创建数据备份文件 (`mood_log_backup.csv`)。
  * **Safe Operations**: All file I/O is wrapped in a decorator (`@safe_file_operation`) to handle exceptions, ensuring program robustness.
      * **安全操作**: 所有的文件读写都通过装饰器（`@safe_file_operation`）进行异常处理，确保程序的健壮性。

## 🛠️ Tech Stack & Implementation / 技术栈与实现

This project is built purely in Python 3, leveraging several advanced topics and libraries as required by COMP9001.
本项目完全使用 Python 3 实现，并巧妙地利用了几个高级主题和库来完成 COMP9001 的要求：

  * **Core Libraries / 核心库**:
      * `Matplotlib` & `Seaborn`: Used to drive all data visualizations.
          * `Matplotlib` & `Seaborn`: 用于驱动所有的数据可视化图表。
      * `Numpy`: Used to calculate the linear regression (trend line) for the overall trend plot.
          * `Numpy`: 用于计算长期趋势图中的线性回归（趋势线）。
  * **Advanced Topics Implementation / 高级主题实现**:
      * **File I/O (文件 I/O)**:
          * Used the `csv` module for structured data I/O (reading, writing, appending) of the mood log.
              * 使用 `csv` 模块进行结构化数据（心情日志）的读写和追加。
          * Performed standard `.txt` file writing (saving configuration and exporting reports).
              * 进行常规的 `.txt` 文件写入（保存配置 和导出日报）。
          * Used the `json` module for data export.
              * 使用 `json` 模块进行数据导出。
      * **Numpy**:
          * Used `np.polyfit` and `np.poly1d` to calculate and plot the mood trend line.
              * 使用 `np.polyfit` 和 `np.poly1d` 来计算和绘制情绪趋势线。
      * **Modular Design (模块化设计)**:
          * The project has a clean structure, separating concerns (e.g., `data`, `analysis`, `config`) into different directories and `.py` files for maintainability.
              * 项目结构清晰，将不同功能（如 `data`, `analysis`, `config`）分离到不同的目录和 `.py` 文件中，易于维护。
      * **Python Decorators (Python 装饰器)**:
          * A custom `@safe_file_operation` decorator was created and applied to all file-handling functions to centrally manage `PermissionError` and other exceptions, enhancing code robustness.
              * 自定义了 `@safe_file_operation` 装饰器，并将其应用于所有文件处理函数，以统一处理 `PermissionError` 等异常，增强了代码的鲁棒性。

## 📦 Setup & Usage / 如何运行

### 1\. Dependencies / 依赖安装

This project depends on the following Python libraries:
本项目依赖以下 Python 库：

  * `matplotlib`
  * `seaborn`
  * `numpy`

You can install them via pip:
你可以通过 pip 一键安装它们：

```bash
pip install matplotlib seaborn numpy
```

### 2\. Run the Program / 运行程序

After installing the dependencies, run `main.py` in your terminal to start:
安装完依赖后，在你的终端中运行 `main.py` 即可启动程序：

```bash
python main.py
```

### 3\. Project Structure / 程序目录结构

```
ChronoPulse/
│
├── main.py                 # Program entry point / 程序主入口
├── analysis/               # Visualization & reports module / 分析与报告模块
│   ├── daily_analysis.py   # Daily/Monthly charts / 日/月图表
│   ├── reports.py          # Weekly/Daily reports / 周/日报表
│   └── trends.py           # Overall trend analysis / 总趋势分析
│
├── config/                 # Configuration module / 配置模块
│   ├── language.py         # Language settings & strings / 语言设置
│   └── settings.py         # Constants (filenames, moods) / 常量
│
├── data/                   # Data handling module / 数据处理模块
│   └── handlers.py         # Load, save, delete, backup data / 读写数据
│
└── utils/                  # Utility functions / 辅助工具模块
    ├── decorators.py       # Safe file operation decorator / 安全操作装饰器
    └── helpers.py          # Data export functions / 数据导出
```

-----