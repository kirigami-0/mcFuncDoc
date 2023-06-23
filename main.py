import const.common as com


def main():
    # パスを設定する
    config = com.getConfig()
    path = config["datapackPath"]

    # インスタンスを作成
    folderList = com.getFolder(path)
    html = com.docHtml()

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
        baseData = datapack.getDocString(functionList)
        # ドキュメント出力
        html.setHtml(baseData)

main()