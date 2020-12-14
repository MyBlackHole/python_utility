import clr  # add C# suppor

clr.AddReference('DLL\\Http')
clr.AddReference('DLL\\PanGu')
clr.AddReference('DLL\\Time')
clr.AddReference('DLL\\Text')
clr.AddReference('DLL\\Spider')
clr.AddReference('DLL\\Common')
clr.AddReference('DLL\\ArticleText')
clr.AddReference('DLL\\Literal')
from Http import *
from PanGu import *
from Time import *
from Text import *
from Spider import *
from Common import *
from ArticleText import *
from Literal import *

TimeParser = TimeParser


class TextEntity(TextEntity):
    pass


class Article(Article):
    pass


class TextRemover(TextRemover):
    pass


class DoNetUtility(DoNetUtility):
    pass


if __name__ == '__main__':
    print(1)
