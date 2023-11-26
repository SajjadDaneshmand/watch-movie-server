import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SETTINGS_FILE_PATH = os.path.join(BASE_DIR, 'configs.txt')
MSG_FILE_PATH = os.path.join(BASE_DIR, 'messages.txt')


class Settings(object):
    """Settings Class"""
    def __init__(self, setting_type='configs'):
        self._dict = dict()
        self.setting_type = setting_type
        self._load_file()

    def _load_file(self):
        if self.setting_type == 'configs':
            with open(SETTINGS_FILE_PATH, encoding='utf-8') as f:
                lines = f.readlines()
        elif self.setting_type == 'msg':
            with open(MSG_FILE_PATH, encoding='utf-8') as f:
                lines = f.readlines()
        else:
            raise ValueError('The term you want should be either "msg" or "configs"')

        for line in lines:
            line = line.strip()
            key, value = line.split('=')
            setattr(self, key, value)
            self._dict[key] = value

    def as_dict(self):
        return self._dict
