# 定义数据结构
class city:
    def __init__(self, name ):
        self.name = name
        self.theme1=None
        self.theme2=None
        self.theme3=None
        self.theme4=None
        self.themes=None
        self.init_class=None #这里是预设值的分类主题，一共三十个城市，预设成三类（高，中，低）
        self.cluster_class=None

        self.longitude=None
        self.latitude=None

class census_tract:
    def __init__(self, id ):
        self.id = id
        self.theme1=None
        self.theme2=None
        self.theme3=None
        self.theme4=None
        self.themes=None
        self.init_class=None #这里是预设值的分类主题，一共三十个城市，预设成三类（高，中，低）
        self.cluster_class=None

        self.shape=None