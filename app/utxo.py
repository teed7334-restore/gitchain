"""
存放日誌檔案內容bean檔
"""

class UTXO:
    """
    txid: 日誌檔名稱
    txt: 日誌內容，格式 - [日誌等級] [日誌內容] [日誌時間]
    """

    txid = None
    txt = None