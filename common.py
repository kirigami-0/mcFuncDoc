import os
import glob


class docHtml:
    def __init__(self, folderName, fileName):
        self.folderName = folderName
        self.htmlContents = ""
        self.fileName = fileName
        self.page = ""
        self.contentsTree = ""
    
    def setContents(self, data):
        """
        右側の内容を設定する

        Parameters
        ----------
        data : list
            コメントが格納されているリスト
        fileName : str
            ファイルリスト
        """
        for contents in data:
            divClass = ""
            for content in contents:
                divClass += f"""
                <div>
                    {content}
                </div>
                """
        htmlContents = f"""
        <div>
            {divClass}
        </div>
        """
        htmlContents = htmlContents.replace("\n                \n","\n")
        htmlContents = htmlContents.replace("\n            \n","\n")
        htmlContents = htmlContents.replace("\n        <div>","        <div>")
        self.htmlContents = htmlContents

    def setDocHtml(self):
        """
        htmlファイルの内容を設定する。
        """
        self.page = f"""
        <!DOCTYPE html>
        <html lang="ja-JP">
            <head>
                <link rel="stylesheet" href="../../modules/base.module.css" />
                <link rel="stylesheet" href="../../modules/decoration.module.css" />
                <meta lang="jp" />
            </head>
            <body>
                <div class="root white_text">
                    <div class="base_area back_ground">
                        <div class="header_area header">
                            <a class="home title center link_color" href="../index.html">HOME</a>
                            <div class="header_title title center white_text">{self.fileName}</div>
                        </div>
                    <div class="contents_area">
                        <div class="left_area back_ground">
                            {self.contentsTree}
                        </div>
                        <div class="right_area back_ground">
                            {self.htmlContents}
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """


    def setHtml(self):
        """
        htmlファイルを作成する
        """
        self.setDocHtml()
        with open(f"./docs/{self.folderName}/{self.fileName}.html", "w", encoding="utf-8") as f:
            f.write(self.page)



class dataPack:
    def __init__(self):
        self.folderName = []
        self.docStringList = []
        try:
            os.mkdir("./docs")
        except FileExistsError:
            pass


    def getFolder(self, path):
        """
        フォルダー名を取得する。

        Parameters
        ----------
        path : str
            パス
        """
        ignoreFile = ("LICENSE", "data")
        for entry in os.scandir(path):
            # フォルダーのみを取得する
            if entry.is_dir():
                if not entry.name.startswith(".") and not entry.name in ignoreFile:
                    self.folderName.append(entry.name)
    

    def getFuntionList(self, path, folderName):
        """
        mcfunctionファイルパスを取得する

        Parameters
        ----------
        path : str
            パス
        folderName : str
            フォルダー名
        
        returns
        -------
        replaseFuncList : list
            ファイルパス
        """

        # ファイルパスを取得する
        functionFiles = glob.glob(f"{path}/{folderName}" + "/**/*.mcfunction", recursive=True)
        replaseFuncList = []
        # 区切り文字を変更する
        for function in functionFiles:
            replaseFuncList.append(function.replace("\\", "/"))
        return replaseFuncList
    

    def readFile(self, filePath):
        """
        mcfunctionファイルパスを取得する

        Parameters
        ----------
        filePath : str
            ファイルパス
        
        returns
        -------
        docStringList : list
            コメントリスト
        """
        fileList = []
        docStringList = []
        isDocString = False
        # ファイルを行ごとに読み込む
        with open(filePath, "r", encoding="utf-8") as f:
            lineTextList = f.readlines()

        for lineText in lineTextList:
            lineText = lineText.split("\n")[0]
            if lineText.startswith("#>"):
                isDocString = True
                fileList.append(lineText)

            elif lineText.startswith("#") and isDocString:
                fileList.append(lineText)

            elif isDocString:
                isDocString = False
                docStringList.append(fileList)
                fileList = []
        return docStringList


    def getDocString(self, folderName, functionList):
        """
        docStringを取得する

        Parameters
        ----------
        folderName : str
            フォルダー名
        functionList : list
            mcfunctionが格納されたリスト
            
        returns
        -------
        docStringList : list
            コメントリスト
        """

        try:
            os.mkdir(f"./docs/{folderName}")
        except FileExistsError:
            pass
        docStringList = []
        for functionPath in functionList:
            docStringList.append(self.readFile(functionPath))
        return docStringList

    def setContents(self, docStringList, folderName):
        """
        docStringを取得する

        Parameters
        ----------
        docStringList : list
            コメントリスト
        folderName : str
            フォルダー名
        """

        for data in docStringList:
            if data:
                fileName = data[0][0]
                fileName = fileName[fileName.find(":") + 1 :].replace("/", "-")
                html = docHtml(folderName, fileName)
                html.setContents(data)
                html.setHtml()
