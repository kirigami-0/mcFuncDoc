import glob
import json
import os
import const.html as html

def getConfig():
    """
    設定ファイルを読み取る

    Returns
    -------
    config : dict
        設定データ
    """
    config = controlFile("./config.json", "r")
    config = json.loads(config)
    return config


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


def controlFile(path, mode, fileData={}):
    """ファイルを操作する

    Parameters
    ----------
    path : str
        ファイルパス
    mode : str
        モード
    fileData : str, optional
        ファイルデータ, by default ""

    Returns
    -------
    file : str
        ファイルデータ
    """
    read = ("r", "r+")
    write = ("w", "w+", "a", "a+")
    with open(path, mode, encoding="utf-8") as f:
        if mode in read:
            file = f.read()
        elif mode in write:
            file = f.write(fileData)
    return file


def makeFolder(path):
    """フォルダ作成

    Parameters
    ----------
    path : str
        作成したいパス
    """
    os.makedirs(path, exist_ok=True)


def setAnnotation(annotations):
    """アノテーション用のCSSを作成する

    Parameters
    ----------
    annotations : dict
        config上のアノテーションカラー
    """
    annotationsColor = ""
    for key, color in annotations.items():
        className = ".%(KEY) {\n\tcolor: %(COLOR); \n}\n"
        className = className.replace("%(KEY)", key[1:]).replace("%(COLOR)", color)
        annotationsColor += className
    controlFile("modules/annotation.module.css", "w", annotationsColor)

class dataPack:
    def __init__(self, folderName):
        self.docData = {
            "folderName": folderName,
            "page": [],
            "index":[]
        }
        self.htmlData = html.HTML()

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
        functionFiles = glob.glob(f"{path}/{folderName}/**/*.mcfunction", recursive=True)
        replaseFuncList = []
        # 区切り文字を変更する
        for function in functionFiles:
            function = function.replace("//", "/").replace("\\", "/")
            replaseFuncList.append(function)
        return replaseFuncList


    def getDocString(self, functionList):
        """ドキュメントデータを作成する

        Parameters
        ----------
        functionList : list
            ファンクションリスト

        Returns
        -------
        docData : dict
            ドキュメントデータ
        """
        indexData = ''
        for functionPath in functionList:
            pageData = self.readFile(functionPath)
            indexData += self.getIndex(functionPath)
            self.docData["page"].append(pageData)
        self.docData["index"] = indexData
        return self.docData

    def checkAnnotation(self, text):
        """アノテーションを設定する

        Parameters
        ----------
        text : str
            テキスト

        Returns
        -------
        text : str
            テキスト
        """
        text = text.replace("@user", self.htmlData.setSpan("user", "@user"))
        text = text.replace("@public", self.htmlData.setSpan("public", "@public"))
        text = text.replace("@api", self.htmlData.setSpan("api", "@api"))
        text = text.replace("@context", self.htmlData.setSpan("context", "@context"))
        text = text.replace("@within", self.htmlData.setSpan("within", "@within"))
        text = text.replace("@handles", self.htmlData.setSpan("handles", "@handles"))
        text = text.replace("@patch", self.htmlData.setSpan("patch", "@patch"))
        text = text.replace("@input", self.htmlData.setSpan("input", "@input"))
        text = text.replace("@output", self.htmlData.setSpan("output", "@output"))
        text = text.replace("@reads", self.htmlData.setSpan("reads", "@reads"))
        text = text.replace("@writes", self.htmlData.setSpan("writes", "@writes"))
        text = text.replace("@private", self.htmlData.setSpan("private", "@private"))
        return text
        
    def readFile(self, filePath):
        """
        mcfunctionファイルパスを取得する

        Parameters
        ----------
        filePath : str
            ファイルパス
        
        returns
        -------
        docStringDict : dict
            コメント情報が乗った辞書
        """
        # ファイルを行ごとに読み込む
        with open(filePath, "r", encoding="utf-8") as f:
            lineTextList = f.readlines()

        isDocString = False
        filePath = filePath.split("functions/")[-1].replace(".mcfunction","").replace("/","-")
        pageData = {
            "fileName": filePath,
            "contents": ""
        }
        
        contentsBlock = ''
        for lineText in lineTextList:
            lineText = lineText.split("\n")[0].replace(" ", self.htmlData.space)
            if (lineText.startswith("#>")) or (lineText.startswith("#") and isDocString):
                isDocString = True
                # アノテーションのチェックを行う
                lineText = self.checkAnnotation(lineText)
                contentsBlock += self.htmlData.setDocBlock(lineText, 6)
            elif isDocString:
                isDocString = False
                contents = self.htmlData.setDiv("contents", contentsBlock[:-1], 5)
                pageData["contents"] = contents[:-1]
                contentsBlock = ''
        return pageData

    def getIndex(self, filePath):
        """目次エリアを作成する

        Parameters
        ----------
        filePath : str
            ファイルパス

        Returns
        -------
        indexData: str
            HTMLデータ
        """
        indexName = filePath.split("functions")[-1][1:]
        indexName = indexName.replace("/", "-").replace(".mcfunction", "")
        indexData = self.htmlData.setIndexData("index index_color", "link link_area", indexName, f"{indexName}.html", 6)
        return indexData[:-1]

    def makeHtml(self, file, docData, folderName, theme):
        """HTMLファイルを作成する

        Parameters
        ----------
        file : str
            HTMLデータ
        docData : dict
            ドキュメントデータ
        folderName : str
            フォルダ名
        theme : str
            テーマ
        """
        for page in docData["page"]:
            file = controlFile("./const/template.html", "r")
            fileName = page["fileName"]
            contents = page["contents"]
            file = self.htmlData.setContents(file, contents)
            file = self.htmlData.setTitle(file, fileName)
            file = self.htmlData.setIndex(file, docData["index"])
            file = self.htmlData.setTheme(file, theme)
            makeFolder(f"./docs/{folderName}")
            controlFile(f"./docs/{folderName}/{fileName}.html", "w", file)
        
        # 目次を作成する
        file = controlFile("./const/template.html", "r")
        file = self.htmlData.setContents(file, "")
        file = self.htmlData.setTitle(file, folderName)
        file = self.htmlData.setIndex(file, docData["index"])
        file = self.htmlData.setTheme(file, theme)
        controlFile(f"./docs/{folderName}/INDEX.html", "w", file)
    
    def makeHome(self, folderList, theme):
        """HOMEを作成する

        Parameters
        ----------
        folderList : list
            フォルダリスト
        theme : str
            テーマ
        """
        file = controlFile("./const/HOME.html", "r")
        index = ""
        for folderName in folderList:
            index += self.htmlData.setIndexData("index index_color", "link link_area", folderName, f"{folderName}/INDEX.html", 6)
        file = self.htmlData.setIndex(file, index)
        file = self.htmlData.setTheme(file, theme)
        controlFile(f"./docs/HOME.html", "w", file[:-1])