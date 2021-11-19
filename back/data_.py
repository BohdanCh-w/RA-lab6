from json import load


class DataRetriever:
    __ui = None
    __crt = None
    __exp = None

    ui_path = r'data\ui_uk.json'
    crt_path = r'data\criterias.json'
    exp_path = r'data\experts.json'

    @classmethod
    def set_ui_lang(cls, path):
        cls.ui_path = path
        cls.__ui = None

    @classmethod
    def ui(cls, attr=None):
        if cls.__ui is None:
            with open(cls.ui_path, 'r', encoding='utf-8') as f:
                cls.__ui = load(f)
        if attr is None:
            return cls.__ui
        return cls.__ui[attr]

    @classmethod
    def crt(cls):
        if cls.__crt is None:
            with open(cls.crt_path, 'r', encoding='utf-8') as f:
                cls.__crt = load(f)
        return cls.__crt

    @classmethod
    def exp(cls):
        if cls.__exp is None:
            with open(cls.exp_path, 'r', encoding='utf-8') as f:
                cls.__exp = load(f)
        return cls.__exp
