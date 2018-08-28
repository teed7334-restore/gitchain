"""
日誌處理程式
"""

import os
import time
import uuid


class Log:

    def write_log(self, params, utxo):
        """
        寫入日誌

        Args:
            params: params.py 物件
            utxo: utxo.py 物件

        Returns:
            utxo: utxo.py 物件
        """

        txid = str(uuid.uuid4())
        txt = "[" + params.level + "] " + params.content + " " + params.create_at
        f = open('block/' + txid, 'w')
        f.close()
        utxo.txid = txid
        utxo.txt = txt
        return utxo

    def remove_log(self, utxo):
        """
        移除日誌

        Args:
            utxo: utxo.py 物件
        
        Returns:
            None
        """

        os.remove('block/' + utxo.txid)
