"""
存放網頁Post資料bean檔
"""

class Params:
    """
    create_at: 新增日期
    level: 日誌等級，例如 - emergency, alert, critical, error, warning, notice, info, debug
    content: 日誌內容
    """

    create_at = None
    level = None
    content = None
    