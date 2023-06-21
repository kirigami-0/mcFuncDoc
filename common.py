import os
import glob
import json

class docHtml:
    def __init__(self):
        try:
            os.mkdir("./docs")
        except FileExistsError:
            pass
        self.page = ""
        self.fileName = ""
        self.folderName = ""


    def setContents(self, baseData):
        """
        右側の内容を設定する

        Parameters
        ----------
        baseData : dict
            コメントが格納されているリスト
        fileName : str
            ファイルリスト
        """
        self.folderName = baseData["folderName"]
        for contents in baseData["contents"]:
            self.fileName = contents["fileName"]
            for docStringBlock in contents["docString"]:
                docBlock = ""
                for docStringList in docStringBlock:
                    divContents = ""
                    for docString in docStringList:
                        divContents += f"""\t\t\t\t\t\t\t\t<div>{docString}</div>\n"""
                    docBlock += f"""\t\t\t\t\t\t\t<div class="A">\n{divContents}\t\t\t\t\t\t\t</div>\n"""
                    self.setDocHtml(docBlock)
                    self.setHtml()

    def setDocHtml(self, docBlock, contentsTree=""):
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
                            {contentsTree}
                        </div>
                        <div class="right_area back_ground">
{docBlock}
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
        try:
            os.mkdir(f"./docs/{self.folderName}")
        except FileExistsError:
            pass
        print(f"{self.folderName}/{self.fileName}")
        with open(f"./docs/{self.folderName}/{self.fileName}.html", "w", encoding="utf-8") as f:
            f.write(self.page)




def getConfig():
    """
    設定ファイルを読み取る

    Returns
    -------
    config : dict
        設定データ
    """
    with open("./config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


class dataPack:
    def __init__(self, folderName):
        self.baseData = {
            "folderName": folderName,
            "contents": []
        }
        
    
    def getDocString(self, functionList):
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

        for functionPath in functionList:
            contents = {
                "fileName": "",
                "docString": []
            }
            fileName = functionPath.split("/")[-1]
            fileName = fileName[:fileName.find(".")]
            contents["fileName"] = fileName
            contents["docString"].append(self.readFile(functionPath))
            self.baseData["contents"].append(contents)

        return self.baseData


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




def getFolder(path):  
    """データパックのフォルダ名を取得する

    Parameters
    ----------
    path : str
        パス

    Returns
    -------
    folderList : list
        フォルダリスト
    """
    ignoreFile = ("LICENSE", "data")
    folderList = []
    for entry in os.scandir(path):
        # フォルダーのみを取得する
        if entry.is_dir():
            if not entry.name.startswith(".") and not entry.name in ignoreFile:
                folderList.append(entry.name)
    return folderList
