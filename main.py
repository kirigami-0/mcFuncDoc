import common as com


def main():
    # パスを設定する
    path = ''

    # インスタンスを作成
    doc = com.dataPack()
    doc.getFolder(path)

    # 単体のデータパックを指定した場合パスを修正する
    if not doc.folderName:
        modifyPath = path.split("/")[0:-1]
        doc.folderName.append(path.split("/")[-1])
        path = ""
        for data in modifyPath:
            path += f"{data}/"
        path.strip()

    # htmlファイルを作成する
    for folderName in doc.folderName:
        functionList = doc.getFuntionList(path, folderName)
        docStringList = doc.getDocString(folderName, functionList)
        doc.setContents(docStringList, folderName)

main()