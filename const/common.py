import glob
import json
import os
from ast import literal_eval

class Html:
    def __init__(self) -> None:
        self.tab = "\t"
        self.ln = "\n"
        self.space = "&emsp;"
        self.div = f'<div class="%(DIV_CLASS)">%(DIV_VALUE)</div>'
        self.a = f'<a class=%(A_ClASS) href="%(A_PATH)">%(A_VALUE)</a>'
    
    def replaceValue(self, value, divData="", aData=""):
        """データを置き換える

        Parameters
        ----------
        value : str
            置き換え前データ
        divData : dict
            divの置き換えデータ
        aData : dict
            aタグの置き換えデータ

        Returns
        -------
        value : str
            置き換え済みデータ
        """
        if divData:
            value = value.replace("%(DIV_CLASS)", divData["divClass"] if divData["divClass"] else '""')
            value = value.replace("%(DIV_VALUE)", divData["divValue"] if divData["divValue"] else '""')
        if aData:
            value = value.replace("%(A_ClASS)", aData["aClass"] if aData["aClass"] else '""')
            value = value.replace("%(A_VALUE)", aData["aValue"] if aData["aValue"] else '""')
            value = value.replace("%(A_PATH)", aData["aPath"] if aData["aPath"] else '""')
        return value
    
    def getReplaceData(self):
        divData = {
            "divClass": "",
            "divValue": ""
        }
        aData = {
            "aClass": "",
            "aValue": "",
            "aPath": "",
        }

        return divData, aData

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


def controlFile(path, mode, fileData=""):
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

class dataPack:
    def __init__(self, folderName):
        self.baseData = {
            "folderName": folderName,
            "contents": [],
        }

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
        """
        docStringを取得する

        Parameters
        ----------
        functionList : list
            mcfunctionが格納されたリスト
            
        returns
        -------
        baseData : dict
            ドキュメント化するファイルのデータ
        """

        for functionPath in functionList:
            # filrName = functionPath.split("/")[-1].replace(".mcfunction", "")
            docStringDict = self.readFile(functionPath)
            if docStringDict["docStringList"]:
                self.baseData["contents"].append(docStringDict)
        return self.baseData

    def checkAnnotation(self, text, divData):
        divData["divValue"] = text
        if "@user" in text:
            divData["divClass"] = "user"
        elif "@public" in text:
            divData["divClass"] = "public"
        elif "@api" in text:
            divData["divClass"] = "api"
        elif "@context" in text:
            divData["divClass"] = "context"
        elif "@within" in text:
            divData["divClass"] = "within"
        elif "@handles" in text:
            divData["divClass"] = "handles"
        elif "@patch" in text:
            divData["divClass"] = "patch"
        elif "@input" in text:
            divData["divClass"] = "input"
        elif "@output" in text:
            divData["divClass"] = "output"
        elif "@reads" in text:
            divData["divClass"] = "reads"
        elif "@writes" in text:
            divData["divClass"] = "writes"
        elif "@private" in text:
            divData["divClass"] = "private"
        else:
            divData["divClass"] = "normal"
        return divData
        
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
        comment = ""
        filePath = filePath.split("functions/")[-1].replace(".mcfunction","")
        filePath = filePath.replace("/","-")
        docStringDict = {
            "fileName": filePath,
            "docStringList": []
        }
        html = Html()
        divData, aData = html.getReplaceData()
        for lineText in lineTextList:
            lineText = lineText.split("\n")[0].replace(" ", html.space)
            if (lineText.startswith("#>")) or (lineText.startswith("#") and isDocString):
                isDocString = True
                # アノテーションのチェックを行う
                divData = self.checkAnnotation(lineText, divData)
                # html要素を作成する
                repComment = f"{html.tab * 6}{html.div}{html.ln}"
                repComment = html.replaceValue(repComment, divData)
                comment += repComment
            elif isDocString:
                isDocString = False
                docStringDict["docStringList"].append(comment)
                comment = ""
        return docStringDict


class docHtml():
    def __init__(self, config):
        self.config = config
        
        annotations = ""
        for annotation in config["annotationsColor"].items():
            value = annotation[0][1:]
            color = annotation[1]
            annotations += f".{value} {{\n\tcolor: {color};\n}}\n"
        controlFile("./modules/annotation.module.css", "w", annotations)

    def getTemplate(self, isHome=False):
        """
        HTMLファイルを取得する

        Returns
        -------
        file: str
            ファイル
        """
        if isHome:
            with open("./const/HOME.html", "r", encoding="utf-8") as f:
                file = f.read()
        else:
            with open("./const/template.html", "r", encoding="utf-8") as f:
                file = f.read()
        return file.replace("%(theme)",self.config["theme"])
    

    def setIndex(self, value, linkPath):
        """
        目次を作成する

        Parameters
        ----------
        value : str
            リンクの名前
        linkPath : str
            リンクのパス
        """
        html = Html()

        indexData = f"{html.tab * 5}{html.div}{html.ln}"
        indexData = html.replaceValue(indexData)

    def setHtml(self, baseData):
        """
        HTMLファイルを設定する

        Parameters
        ----------
        baseData : dict
            ドキュメント用のデータが格納された事象
        """
        html = Html()
        divData, aData =html.getReplaceData()
        # 目次を作成
        indexData = ""
        for index in baseData["contents"]:
            aData["aValue"] = index["fileName"]
            aData["aClass"] = "link_color"
            aData["aPath"] = f"./{index['fileName']}.html"
            data = f"{html.tab * 6}{html.a}{html.ln}"
            data = html.replaceValue(data, aData=aData)
            divData["divClass"] = "link link_area"
            divData["divValue"] = f"{html.ln}{data}{html.tab * 5}"
            div = f"{html.tab * 5}{html.div}{html.ln}"
            div = html.replaceValue(div, divData)
            indexData += div
        
        # 内容を作成
        for data in baseData["contents"]:
            title = f"{baseData['folderName']}:{data['fileName']}"
            divData["divClass"] = "contents"
            contents = ""
            for string in data["docStringList"]:
                stringBlock = f"{html.tab * 5}{html.div}{html.ln}"
                divData["divValue"] = f"{html.ln}{string}{html.tab * 5}"
                stringBlock = html.replaceValue(stringBlock, divData)
                contents += stringBlock
            file = self.getTemplate()
            file = self.setContents(file, contents[: -1], title, indexData[:-1])
            self.writeHtml(baseData['folderName'], data['fileName'], file)
        # return indexData


    def setHome(self, folderList):
        file = self.getTemplate(True)
        title = "HOME"
        index = ""
        for folderName in folderList:
            index += self.setIndex(folderName, f"./{folderName}/Index.html")
        file = self.setContents(file, "", title, index)
        self.writeHtml("", "HOME", file)


    def setContents(self, file, contents, title, index):
        """ファイルコンテンツを設定する

        Parameters
        ----------
        file : str
            ファイル
        contents : str
            ドキュメント本体
        title : str
            タイトル
        index : str
            目次

        Returns
        -------
        file : str
            HTMLファイル情報
        """
        file = file.replace("%(TITLE)", title)
        file = file.replace("%(CONTENTS)", contents)
        file = file.replace("%(INDEX)", index)
        return file
    
    def writeHtml(self, folderName, fileName, fileData):
        """HTMLファイルを出力する

        Parameters
        ----------
        folderName : str
            フォルダ名
        fileName : str
            ファイル名
        fileData : str
            ファイルデータ
        """
        makeFolder(f"./docs/{folderName}")
        controlFile(f"./docs/{folderName}/{fileName}.html", "w", fileData)

