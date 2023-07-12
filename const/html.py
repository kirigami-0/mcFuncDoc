class HTML:
    def __init__(self):
        self.tab = "\t"
        self.ln = "\n"
        self.space = "&emsp;"

    def setIndexData(self, aClassName, divClassNeme, value, link, count=0):
        """目次を用のHTMLデータを作成する

        Parameters
        ----------
        aClassName : str
            アンカータグ用のクラス名
        divClassNeme : str
            div側のクラス名
        value : str
            内容
        link : str
            リンクパス
        count : int, optional
            タブの数, by default 0

        Returns
        -------
        data : str
            HTMLデータ
        """
        tab = self.tab * count
        data = f'{tab}<div class="{divClassNeme}">{self.ln}'
        if aClassName:
            data += f'{tab}{self.tab}<a class="{aClassName}" href="{link}">{self.ln}'
        else:
            data += f'{tab}<a href="{link}">{self.ln}'
        data += f'{tab}{self.tab * 2}{value}{self.ln}'
        data += f'{tab}{self.tab}</a>{self.ln}'
        data += f'{tab}</div>{self.ln}'

        return data
    
    def setSpan(self, className, value, count=0):
        """spanタグを作成する

        Parameters
        ----------
        className : str
            クラス名
        value : str
            内容
        count : int, optional
            タブの数, by default 0

        Returns
        -------
        data : str
            spanデータ
        """
        tab = self.tab * count
        if className:
            data = f'{tab}<span class="{className}">'
        else:
            data = f'{tab}<span>'
        data += f'{value}'
        data += f'</span>'
        return data
    
    def setDiv(self, className, value='', count=0):
        """divクラスを作成する

        Parameters
        ----------
        className : str
            クラス名
        value : str, optional
            内容, by default ''
        count : int, optional
            タブの数, by default 0

        Returns
        -------
        data : str
            divクラス
        """
        tab = self.tab * count
        if className:
            data = f'{tab}<div class="{className}">{self.ln}'
        else:
            data = f'{tab}<div>{self.ln}'
        data += f'{value}{self.ln}'
        data += f'{tab}</dav>{self.ln}'
        return data
    
    def setDocBlock(self, value, count=0):
        """コンテンツブロックを作成する

        Parameters
        ----------
        value : str
            内容
        count : int, optional
            タブの数, by default 0

        Returns
        -------
        data : str
            ブロックコンテンツ
        """
        data = f'{self.tab * count}<div>{value}</div>{self.ln}'
        return data

    def setContents(self, html, contents):
        """コンテンツ

        Parameters
        ----------
        html : str
            HTMLデータ
        contents : str
            コンテンツ

        Returns
        -------
        html : str
            HTMLデータ
        """
        html = html.replace("%(CONTENTS)", contents)
        return html
    
    def setIndex(self, html, index):
        """目次を作成する

        Parameters
        ----------
        html : str
            HTMLデータ
        index : str
            内容

        Returns
        -------
        data : str
            HTMLデータ
        """
        html = html.replace("%(INDEX)", index)
        return html
    
    def setTitle(self, html, title):
        """タイトルを設定する

        Parameters
        ----------
        html : str
            HTMLデータ
        title : str
            タイトル

        Returns
        -------
        html : str
            HTMLデータ
        """
        html = html.replace("%(TITLE)", title)
        return html
    
    def setTheme(self, html, theme):
        """テーマを設定する

        Parameters
        ----------
        html : str
            HTMLデータ
        theme : str
            テーマ

        Returns
        -------
        html : str
            HTMLデータ
        """
        html = html.replace("%(THEME)", theme)
        return html
