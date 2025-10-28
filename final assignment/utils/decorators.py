def safe_file_operation(func):
    """装饰器用于安全处理文件操作"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError:
            print("错误: 没有文件写入权限")
            return None
        except Exception as e:
            print(f"发生未知错误: {e}")
            return None
    return wrapper