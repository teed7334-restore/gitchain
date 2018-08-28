"""
Restful API 主程式
"""

import os
import shutil
import time
import uuid

from flask import Flask, request

import setting
from log import *
from params import *
from upload import *
from utxo import *

app = Flask(__name__)

git = Upload()
log = Log()

@app.route('/', methods=['GET'])
def make_first_block():
    """
    建立創世區塊

    Args:
        None

    Returns:
        1:成功 | 0:失敗
    """

    if False == check_block_directory():
        git.clone()
        return "1"
    else:
        return "0"

@app.route('/write', methods=['GET', 'POST'])
def write():
    """
    寫入日誌

    Args:
        create_at: 新增日期
        level: 日誌等級，例如 - emergency, alert, critical, error, warning, notice, info, debug
        content: 日誌內容

    Returns:
        1:成功 | 0:失敗
    """

    to_branch = get_default_branch_name()

    if False == check_block_on_branch():
        """
        如果目前所在的Branch與預設Branch不符時
        """

        git.new_branch(to_branch)

    if 'POST' == request.method:
        """
        當Client端透過HTTP POST過來時
        """

        params = bind_post_params()
        utxo = UTXO()
        utxo = log.write_log(params, utxo)
        content = utxo.txt
        git.commit(content)
        log.remove_log(utxo)
        return '1'
    else:
        return '0'

@app.route('/make_block', methods=['GET'])
def make_block():
    """
    上鏈，複製本地日誌檔資料夾成一新資料夾，新資料夾名採用UUID命名，進入該資料夾之後，透過git push將資料打去remote branch

    Args:
        None

    Returns:
        1:成功 | 0:失敗
    """

    backup = Upload()
    old_directory = os.getenv('DIRECTORY')
    to_branch = get_default_branch_name()
    new_directory = str(uuid.uuid4())
    shutil.copytree(old_directory, new_directory, True)
    backup.set_repo(new_directory)
    backup.pull()
    backup.push(to_branch)
    shutil.rmtree(new_directory)
    return "1"

def check_block_directory():
    """
    檢查日誌檔存放所需資料夾是否存在

    Args:
        None

    Returns:
        1:成功 | 0:失敗
    """

    directory = str(os.getenv('DIRECTORY'))
    if os.path.isdir(directory):
        return True
    else:
        return False

def check_block_on_branch():
    """
    檢查當前所在Branch是否與預設Branch不同

    Args:
        None

    Returns:
        1:成功 | 0:失敗
    """

    branch = git.get_branch()
    to_branch = get_default_branch_name()
    if to_branch == branch:
        return True
    else:
        return False

def bind_post_params():
    """
    將使用者透過HTTP POST傳過來之變數，綁定到params.py物件

    Args:
        create_at: 新增日期
        level: 日誌等級，例如 - emergency, alert, critical, error, warning, notice, info, debug
        content: 日誌內容

    Returns:
        params.py 物件
    """

    params = Params()
    params.create_at = str(request.form['create_at'])
    params.level = str(request.form['level'])
    params.content = str(request.form['content'])
    return params

def get_default_branch_name():
    """
    取得預設Branch名稱

    Args:
        None

    Returns:
        Branch名稱
    """

    branch_name = str(os.getenv('NODE')) + '-' + str(time.strftime("%Y%m%d", time.localtime()))
    return branch_name
