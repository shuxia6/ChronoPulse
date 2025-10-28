# 常量定义
DATA_FILE = "mood_log.csv"
CONFIG_FILE = "config.txt"
BACKUP_FILE = "mood_log_backup.csv"

# 心情分数和有效值常量
MOOD_SCORES = {
    "开心": 3, "Happy": 3,
    "一般": 2, "Neutral": 2,
    "压力大": 1, "Stressed": 1
}

# 程序的有效心情列表
VALID_MOODS = list(MOOD_SCORES.keys())

MOOD_MAP = {
    "zh": {1: "开心", 2: "一般", 3: "压力大"},
    "en": {1: "Happy", 2: "Neutral", 3: "Stressed"}
}
