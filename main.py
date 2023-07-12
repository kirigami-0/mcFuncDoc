import const.common as com

def main():
    # パスを設定する
    config = com.getConfig()
    path = config["datapackPath"]

    # インスタンスを作成
    folderList = com.getFolder(path)
    page = com.controlFile('const/template.html', 'r')
    # アノテーション用のCSSを作成する
    com.setAnnotation(config["annotationsColor"])

    # 単体のデータパックを指定した場合パスを修正する
    if not folderList:
        modifyPath = path.split("/")[0:-1]
        folderList.append(path.split("/")[-1])
        path = ""
        for data in modifyPath: 
            path += f"{data}/"

    for folderName in folderList:
        # フォルダごとにインスタンスを作成する
        datapack = com.dataPack(folderName)
        functionList = datapack.getFuntionList(path, folderName)
        # ドキュメント化可能なデータを取得する
        docData = datapack.getDocString(functionList)
        # ドキュメント出力
        datapack.makeHtml(page, docData, folderName, config["theme"])
    
    datapack.makeHome(folderList, config["theme"])
main()