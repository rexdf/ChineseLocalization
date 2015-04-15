import sublime
import sublime_plugin
import os
from hashlib import md5

CONFIG_NAME = "Localization.sublime-settings"

LANGS = {
    "ZH_CN": {
        'zipfile': 'ZH_CN.zip',
        'syntax_md5sum': '44cd99cdd8ef6c2c60c0a89d53a40b95'
    },
    "ZH_TW": {
        "zipfile": "ZH_TW.zip",
        'syntax_md5sum': "fe7457cfd227b7db74e785321f672c4a"
    },
    "EN": {
        "zipfile": "EN.zip",
        'syntax_md5sum': "2667c3fe5c1102274051920b1f581adb"
    }
}


def get_language_setting():
    config = sublime.load_settings(CONFIG_NAME)
    lang = config.get('language', None)
    if lang not in LANGS:
        lang = None
    return lang


def restore_language_setting(lang):
    config = sublime.load_settings(CONFIG_NAME)
    config.set("language", lang)
    sublime.save_settings(CONFIG_NAME)


def init():
    lang = get_language_setting()
    set_language(lang)


def set_language(lang):
    if not lang:
        return
    PACKAGES_PATH = sublime.packages_path()
    DEFAULT_PATH = os.path.join(PACKAGES_PATH, "Default")
    SYN_PATH = os.path.join(DEFAULT_PATH, "Syntax.sublime-menu")

    if os.path.isfile(SYN_PATH):
        with open(SYN_PATH, "rb") as f:
            syntax = f.read()
        m = md5()
        m.update(syntax)
        if m.hexdigest() == LANGS[lang]['syntax_md5sum']:
            sublime.status_message("%s has loaded." % lang)
            return
    # mkdir if Default not exist
    if not os.path.isdir(DEFAULT_PATH):
        os.mkdir(DEFAULT_PATH)
    # Load binary resource
    PACKAGE_NAME = os.path.basename(os.path.dirname(__file__)).split('.')[0]
    LOCALZIP_RES = "Packages/{}/{}".format(PACKAGE_NAME,
                                           LANGS[lang]['zipfile'])
    lang_bytes = sublime.load_binary_resource(LOCALZIP_RES)
    # write to tempfile and unzip it.
    import zipfile
    from tempfile import NamedTemporaryFile
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.write(lang_bytes)
    tmp_file.close()
    with zipfile.ZipFile(tmp_file.name, "r") as f:
        f.extractall(DEFAULT_PATH)
    tmp_file.close()
    os.unlink(tmp_file.name)


class ToggleLanguageCommand(sublime_plugin.ApplicationCommand):

    def run(self, language):
        set_language(language)
        restore_language_setting(language)

    def is_checked(self, language):
        return get_language_setting() == language


def plugin_loaded():
    """Load and unzip the files."""
    sublime.set_timeout(init, 200)