import glob
import json
import os

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
        filePath = filePath.split("/")[-1].replace(".mcfunction","")
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

    def getTemplate(self):
        """
        HTMLファイルを取得する

        Returns
        -------
        file: str
            ファイル
        """
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

        for data in baseData["contents"]:
            title = f"{baseData['folderName']}:{data['fileName']}"
            stringBlock = ""
            for string in data["docStringList"]:
                stringBlock += f"""\t\t\t<div class="contents">\n{string}\t\t\t</div>\n"""
            file = self.getTemplate()
            file = self.setContents(file, stringBlock[-1], title)
            self.writeHtml(baseData['folderName'], data['fileName'], file)


    def setContents(self, file, contents, title, index=""):
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
        with open(f"./docs/{folderName}/{fileName}.html", "w", encoding="utf-8") as f:
            f.write(fileData)

