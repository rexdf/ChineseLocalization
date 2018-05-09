import sublime
import sublime_plugin
import os
from hashlib import md5

__version__ = "1.11.2"

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
    "de_DE": {
        "zipfile": "de_DE.zip",
        'syntax_md5sum': "2b1256d95592a5c2a517e86d4be2e4cf"
    },
    "es_ES": {
        "zipfile": "es_ES.zip",
        'syntax_md5sum': "9ae95c10fda7a268dba6f3deb1d7045e"
    },
    "fr_FR": {
        "zipfile": "fr_FR.zip",
        'syntax_md5sum': "d01201fb6fc53dd28fc6f48a9bb3da9d"
    },
    "hy_AM": {
        "zipfile": "hy_AM.zip",
        'syntax_md5sum': "aaea3b150c9dcc9f6fe67ef9740d201d"
    },
    "ru_RU": {
        "zipfile": "ru_RU.zip",
        'syntax_md5sum': "9c3fc2f79bd059749fa221c0d8810c71"
    },
    "sv_SE": {
        "zipfile": "sv_SE.zip",
        'syntax_md5sum': "8e92e8b31f9003c4e494deca2808d23f"
    },
    "Unknown": {
    },
    # "EN": { # This item is deprecated and not used in programming.
    #     "zipfile": "EN.zip",
    #     'syntax_md5sum': (
    #         "2667c3fe5c1102274051920b1f581adb",
    #         "ecd966996f5fcaff6fac2a281bec93d5",  # 3099+
    #     )
    # }
}

BLACK_LIST = {
    "8a2bc3aa52a2d417b42bdc7c80534ce099fc0c65",
    "d8db73c4aa057735e80547773a4293484fd5cb45",
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


def unzip_file(zipfile, dst):
    from zipfile import ZipFile
    with ZipFile(zipfile, "r") as f:
        f.extractall(dst)


def get_builtin_pkg_path():
    base_path = os.path.dirname(sublime.executable_path())
    ret = os.path.join(base_path, 'Packages')
    return ret


def get_file_md5sum(file_path):
    with open(file_path, "rb") as f:
        syntax = f.read()
    m = md5()
    m.update(syntax)
    return m.hexdigest()


def set_language(lang, force=False):
    if lang == "EN":
        is_en = True
    elif lang not in LANGS:
        return
    else:
        is_en = False
    if lang == "Unknown":
        lang = get_setting('language_name')
        sublime.status_message("%s has loaded." % lang)
        return
    PACKAGES_PATH = sublime.packages_path()
    DEFAULT_PATH = os.path.join(PACKAGES_PATH, "Default")
    SYN_PATH = os.path.join(DEFAULT_PATH, "Syntax.sublime-menu")

    # not force update then check current lang
    if not force and os.path.isfile(SYN_PATH):
        syntax_md5sum = get_file_md5sum(SYN_PATH)
        english_ok, other_ok = False, False
        if is_en:
            english_ok = syntax_md5sum == get_setting('en_syntax_md5sum')
        else:
            other_ok = syntax_md5sum == LANGS[lang]['syntax_md5sum']

        if english_ok or other_ok:
            sublime.status_message("%s has loaded." % lang)
            return

    if lang == 'ZH_CN':
        # not evil
        import getpass
        from hashlib import sha1
        usr = getpass.getuser().encode('utf-8')
        m = md5()
        s = sha1()
        m.update(usr)
        s.update(usr)
        res = sha1()
        res.update((s.hexdigest() + m.hexdigest()).encode('utf-8'))
        if res.hexdigest() in BLACK_LIST:
            lang = 'JA_JP'

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
        elif locale_lang[0] in LANGS:
            lang = locale_lang[0]

    # Make sure Default Packages function work
    GOTO_PY = os.path.join(DEFAULT_PATH, 'goto_line.py')
    if is_en or force or not os.path.isfile(GOTO_PY):
        SUBLIME_PACKAGE_PATH = get_builtin_pkg_path()
        DEFAULT_SRC = os.path.join(
            SUBLIME_PACKAGE_PATH, "Default.sublime-package")
        unzip_file(DEFAULT_SRC, DEFAULT_PATH)

    # Load binary resource and unzup it
    if not is_en:
        PACKAGE_NAME = __name__.split('.')[0]
        LOCALZIP_RES = "Packages/{}/{}".format(PACKAGE_NAME,
                                               LANGS[lang]['zipfile'])
        lang_bytes = sublime.load_binary_resource(LOCALZIP_RES)
        # Use BytesIO and zipfile to unzip it.
        from io import BytesIO
        file_buf = BytesIO(lang_bytes)
        unzip_file(file_buf, DEFAULT_PATH)
    else:
        syntax_md5sum = get_file_md5sum(SYN_PATH)
        restore_setting('en_syntax_md5sum', syntax_md5sum)

    MAIN_MENU = os.path.join(DEFAULT_PATH, "Main.sublime-menu")

    # compatible with 3114-
    if not is_en:
        sbt_version = int(sublime.version())
        patch_version = None
        if sbt_version < 3105:
            patch_version = 3065
        elif sbt_version < 3118: #3105~3117
            patch_version = 3105
        elif sbt_version < 3121: #3118~3120
            patch_version = 3118
        elif sbt_version < 3125: #3121~3124
            patch_version = 3121
        elif sbt_version < 3127: #3126
            patch_version = 3126
        elif sbt_version < 3152: #3131
            patch_version = 3131
        if patch_version:
            PATCH_RES = "Packages/{}/patch/{}/{}/Main.sublime-menu.txt".format(
                PACKAGE_NAME, patch_version, lang)
            content = sublime.load_binary_resource(PATCH_RES)
            with open(MAIN_MENU, 'wb') as f:
                f.write(content)

    with open(MAIN_MENU, "rb") as f:
        content = f.read().decode("utf-8")

    # Remove mnemonic for OSX
    import re
    platform = sublime.platform()
    if platform == "osx":
        pattern = re.compile(r"(?<=[\u3000-\u9FFFa-zA-Z])\([A-Za-z]\)", re.M)
        pattern_help = re.compile(r"(ヘルプ|帮助|說明)")

        content = re.sub(pattern, "", content)
        content = re.sub(pattern_help, "Help", content)

        with open(MAIN_MENU, "wb") as f:
            f.write(content.encode("utf-8"))

    # Hack sublime menu
    import json
    content = re.sub(re.compile(r",(?=[\s\r\n]*(}|\]))"), "", content)
    content = re.sub(re.compile(r"^\s*//.*?\n", re.S | re.M), "", content)
    # Hack JA_JP/Main.sublime-menu line 646
    content = re.sub(re.compile(r"(?<=}[, ]) //, \"caption\":.*(?=\n)"),
                     "", content)
    js = json.loads(content, "utf-8")
    for i in range(len(js)):
        del js[i]["children"]
    js = json.dumps(js, ensure_ascii=False, indent=4)

    ZZZZ_LOCALE = os.path.join(PACKAGES_PATH, "ZZZZZZZZ-Localization")
    ZZZZ_SBMENU = os.path.join(ZZZZ_LOCALE, "Main.sublime-menu")
    if not os.path.isdir(ZZZZ_LOCALE):
        os.mkdir(ZZZZ_LOCALE)
    with open(ZZZZ_SBMENU, "wb") as f:
        f.write(js.encode("utf-8"))


class ToggleLanguageCommand(sublime_plugin.ApplicationCommand):

    def run(self, language):
        set_language(language)
        restore_setting("language", language)

    def is_checked(self, language):
        return get_setting('language') == language


def get_command(language, action):
    PACKAGE_NAME = __name__.split('.')[0]
    MENU_RES = "Packages/{}/Menu.json".format(PACKAGE_NAME)
    content = sublime.load_resource(MENU_RES)
    import json
    menu = json.loads(content, "utf-8")
    if language not in menu["supports"]:
        language = "EN"
    return menu["translation"][language][action]


class LocalizeToolCommand(sublime_plugin.WindowCommand):

    def run(self, action, file=None):
        if action == 'open_file':
            sublime.run_command(action, {'file': file})
        elif action == 'new_locale':
            language = self.window.show_input_panel(
                "Input a locale name", "EN", self.on_done_locale, None, None)
        elif action == 'reset':
            pass

    def on_done_locale(self, locale):
        self.__locale = locale
        self.window.show_input_panel(
            "Input a language name", "English", self.on_done_lang, None, None)

    def on_done_lang(self, lang):
        self.__lang = lang
        self.on_done_new()

    def on_done_new(self):
        restore_setting('language_locale', self.__locale)
        restore_setting('language_name', self.__lang)
        restore_setting('language', 'Unknown')

    def description(self, action, file):
        language = get_setting('language')
        return get_command(language, action)


def plugin_loaded():
    """Load and unzip the files."""
    sublime.set_timeout(init, 200)


def cleanup():
    PACKAGES_PATH = sublime.packages_path()
    DEFAULT_PATH = os.path.join(PACKAGES_PATH, "Default")
    ZZZZ_LOCALE = os.path.join(PACKAGES_PATH, "ZZZZZZZZ-Localization")
    import shutil
    shutil.rmtree(DEFAULT_PATH)
    shutil.rmtree(ZZZZ_LOCALE)


def plugin_unloaded():
    PACKAGE_NAME = __name__.split('.')[0]
    from package_control import events

    if events.pre_upgrade(PACKAGE_NAME):
        print('Upgrading from %s!' % events.pre_upgrade(PACKAGE_NAME))
    elif events.remove(PACKAGE_NAME):
        # set_language("EN", True)
        cleanup()
        sublime_plugin.reload_plugin('Default')
        print('Removing %s!' % events.remove(PACKAGE_NAME))
