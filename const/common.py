import glob
import json
import os
from ast import literal_eval

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
            filrName = functionPath.split("/")[-1].replace(".mcfunction", "")
            docStringDict = self.readFile(functionPath)
            if docStringDict["docStringList"]:
                self.baseData["contents"].append(docStringDict)
        return self.baseData


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
        for lineText in lineTextList:
            lineText = lineText.split("\n")[0].replace(" ", "&emsp;")
            if lineText.startswith("#>"):
                isDocString = True
                comment += f"\t\t\t\t<div>{lineText}</div>\n"

            elif lineText.startswith("#") and isDocString:
                comment += f"\t\t\t\t<div>{lineText}</div>\n"

            elif isDocString:
                isDocString = False
                docStringDict["docStringList"].append(comment)
                comment = ""
        return docStringDict


class docHtml():
    def __init__(self):
        pass

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
        return file


    def setHtml(self, baseData):
        """
        HTMLファイルを設定する

        Parameters
        ----------
        baseData : dict
            ドキュメント用のデータが格納された事象
        """
        indexData = ""
        for index in baseData["contents"]:
            indexData += f"""\t\t\t\t\t<div class="index"><a class="link link_color" href="./{index["fileName"]}.html">{index["fileName"]}</a></div>\n"""
        for data in baseData["contents"]:
            title = f"{baseData['folderName']}:{data['fileName']}"
            stringBlock = ""
            for string in data["docStringList"]:
                stringBlock += f"""\t\t\t<div class="contents">\n{string}\t\t\t</div>\n"""
            file = self.getTemplate()
            file = self.setContents(file, stringBlock[:-1], title, indexData[:-1])
            self.writeHtml(baseData['folderName'], data['fileName'], file)
        return indexData

    def setIndex(self, path, folderName, indexData):
        # mcmetaの情報を取ってくる
        with open(f"{path}/{folderName}/pack.mcmeta", "r", encoding="utf-8") as f:
            metaFile = f.read()
        metaFile = literal_eval(metaFile)
        pack_format = metaFile["pack"]["pack_format"]
        description = metaFile["pack"]["description"]
        data = f"""\t\t\t\t\t\t<div>pack_format : {pack_format}</div>\n"""
        data += f"""\t\t\t\t\t\t<div>description : {description}</div>"""
        metaData = f"""\t\t\t\t\t<div class="contents">\n{data}\n\t\t\t\t\t</div>\n"""[:-1]
        file = self.getTemplate()
        file = self.setContents(file, metaData, folderName, indexData[:-1])
        self.writeHtml(folderName, "Index", file)


    def setHome(self, folderList):
        file = self.getTemplate(True)
        title = "HOME"
        index = ""
        for folderName in folderList:
            index += f"""\t\t\t\t\t<div class="index"><a class="link link_color" href="./{folderName}/Index.html">{folderName}</a></div>\n"""
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
        os.makedirs(f"./docs/{folderName}", exist_ok=True)
        with open(f"./docs/{folderName}/{fileName}.html", "w", encoding="utf-8") as f:
            f.write(fileData)

