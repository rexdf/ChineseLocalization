import sublime
import sublime_plugin
import os
from hashlib import md5

__version__ = "1.6.0"

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
    "JA_JP": {
        "zipfile": "JA_JP.zip",
        'syntax_md5sum': "037128b8f8d2616c7239d8e9a7183b4c"
    },
    "EN": {
        "zipfile": "EN.zip",
        'syntax_md5sum': "2667c3fe5c1102274051920b1f581adb"
    }
}


def get_setting(name):
    config = sublime.load_settings(CONFIG_NAME)
    setting = config.get(name, None)
    return setting


def restore_setting(name, value):
    config = sublime.load_settings(CONFIG_NAME)
    config.set(name, value)
    sublime.save_settings(CONFIG_NAME)


def init():
    lang = get_setting('language')
    config_version = get_setting('version')
    # if upgrade to new version force update translation
    if config_version != __version__:
        set_language(lang, force=True)
        restore_setting("version", __version__)
    else:
        set_language(lang)


def set_language(lang, force=False):
    if lang not in LANGS:
        return
    PACKAGES_PATH = sublime.packages_path()
    DEFAULT_PATH = os.path.join(PACKAGES_PATH, "Default")
    SYN_PATH = os.path.join(DEFAULT_PATH, "Syntax.sublime-menu")

    # not force update then check current lang
    if not force and os.path.isfile(SYN_PATH):
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
        # if detect locale override the default only when the first time
        from locale import getdefaultlocale
        locale_lang = getdefaultlocale()
        if locale_lang[0] == "ja_JP":
            lang = "JA_JP"
        elif locale_lang[0] == "zh_TW" or locale_lang[0] == "zh_HK":
            lang = "ZH_TW"
    # Load binary resource
    PACKAGE_NAME = __name__.split('.')[0]
    LOCALZIP_RES = "Packages/{}/{}".format(PACKAGE_NAME,
                                           LANGS[lang]['zipfile'])
    lang_bytes = sublime.load_binary_resource(LOCALZIP_RES)
    # Use BytesIO and zipfile to unzip it.
    from io import BytesIO
    import zipfile
    file_buf = BytesIO(lang_bytes)
    with zipfile.ZipFile(file_buf, "r") as f:
        f.extractall(DEFAULT_PATH)

    MAIN_MENU = os.path.join(DEFAULT_PATH, "Main.sublime-menu")

    fh = open(MAIN_MENU, "rb")
    content = fh.read().decode("utf-8")
    fh.close()

    # Remove mnemonic for OSX
    import re
    platform = sublime.platform()
    if platform == "osx":
        pattern      = re.compile(r"(?<=[\u3000-\u9FFFa-zA-Z])\([A-Za-z]\)", re.M)
        pattern_help = re.compile(r"(ヘルプ|帮助|幫助)")

        content = re.sub(pattern, "", content)
        content = re.sub(pattern_help, "Help", content)

        fh = open(MAIN_MENU, "wb")
        fh.write(content.encode("utf-8"))
        fh.close()

    # Hack sublime menu
    import json
    content = re.sub(re.compile(r",(?=[\s\r\n]*(}|\]))"), "", content)
    content = re.sub(re.compile(r"^\s*//.*?\n", re.S | re.M), "", content)
    js = json.loads(content, "utf-8")
    for i in range(len(js)):
        del js[i]["children"]
    js = json.dumps(js, ensure_ascii=False, indent=4)

    ZZZZ_LOCALE = os.path.join(PACKAGES_PATH, "ZZZZZZZZ-Localization")
    ZZZZ_SBMENU = os.path.join(ZZZZ_LOCALE, "Main.sublime-menu")
    if not os.path.isdir(ZZZZ_LOCALE):
        os.mkdir(ZZZZ_LOCALE)
    fh = open(ZZZZ_SBMENU, "wb")
    fh.write(js.encode("utf-8"))
    fh.close()


class ToggleLanguageCommand(sublime_plugin.ApplicationCommand):

    def run(self, language):
        set_language(language)
        restore_setting("language", language)

    def is_checked(self, language):
        return get_setting('language') == language


def plugin_loaded():
    """Load and unzip the files."""
    sublime.set_timeout(init, 200)
