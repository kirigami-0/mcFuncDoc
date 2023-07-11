class HTML:
    def __init__(self):
        self.tab = "\t"
        self.ln = "\n"
        self.space = "&emsp;"

    def setIndexData(self, aClassName, divClassNeme, value, link, count=0):
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
        tab = self.tab * count
        if className:
            data = f'{tab}<span class="{className}">'
        else:
            data = f'{tab}<span>'
        data += f'{value}'
        data += f'</span>'
        return data
    
    def setDiv(self, className, value='', count=0):
        tab = self.tab * count
        if className:
            data = f'{tab}<div class="{className}">{self.ln}'
        else:
            data = f'{tab}<div>{self.ln}'
        data += f'{value}{self.ln}'
        data += f'{tab}</dav>{self.ln}'
        return data
    
    def setDocBlock(self, value, count=0):
        data = f'{self.tab * count}<div>{value}</div>{self.ln}'
        return data


    def setContents(self, html, contents):
        html = html.replace("%(CONTENTS)", contents)
        return html
    
    def setIndex(self, html, index):
        html = html.replace("%(INDEX)", index)
        return html
    
    def setTitle(self, html, title):
        html = html.replace("%(TITLE)", title)
        return html
    
    def setTheme(self, html, theme):
        html = html.replace("%(THEME)", theme)
        return html
