"""
負責寫入區塊與日誌用物件
"""

import os
from urllib import parse

import setting
from git import Repo


class Upload:

    repo = None
    directory = None
    url = None

    def __init__(self):
        self.directory = str(os.getenv('DIRECTORY'))
        self.url = self.__getRepoUrl()

        if os.path.isdir(self.directory):
            self.set_repo(self.directory)

    def set_repo(self, directory):
        """
        指定Git所在資料夾

        Args:
            directory: Git所在資料夾

        Returns:
            None
        """

        self.repo = Repo(directory)

    def clone(self):
        """
        將遠端的Git資源複製到本地

        Args:
            None

        Returns:
            None
        """

        url = self.__getRepoUrl()
        self.repo = Repo.clone_from(url=url, to_path=self.directory)

    def get_branch(self):
        """
        取得當前所在的Branch名稱

        Args:
            None

        Returns:
            當前所在的Branch名稱
        """

        branch = self.repo.active_branch
        branch = str(branch.name)
        return branch

    def pull(self):
        """
        將遠端Git Branch的資料拉回來

        Args:
            None

        Returns:
            None
        """

        git = self.repo.git
        git.pull()

    def push(self, branch_name):
        """
        將當前所在的Branch資料全數打包推上遠端Branch

        Args:
            branch_name: 遠端branch名稱

        Returns:
            None
        """

        git = self.repo.git
        git.push('origin', branch_name)

    def new_branch(self, branch_name):
        """
        新增一個新的Branch，當Branch存在時，則切換過去

        Args:
            branch_name: 新增的branch名稱

        Returns:
            None
        """

        git = self.repo.git
        git.checkout('origin/master', B=branch_name)

    def commit(self, content):
        """
        提交日誌變動內容

        Args:
            content: 日誌內容

        Returns:
            None
        """

        git = self.repo.git
        git.add('-A')
        self.repo.index.commit(content)

    def __getRepoUrl(self):
        """
        取得遠端預設Branch

        Args:
            None

        Returns:
            None
        """

        url = str(os.getenv('URL'))
        pattern = parse.urlparse(url)
        username = parse.quote(str(os.getenv('USERNAME')))
        password = parse.quote(str(os.getenv('PASSWORD')))
        url = pattern.scheme + '://' + username + ':' + password + '@' + pattern.netloc + pattern.path
        return url
