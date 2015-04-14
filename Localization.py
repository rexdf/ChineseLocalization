import sublime
import sublime_plugin
import zipfile
import os
from hashlib import md5

CONFIG_NAME = "Localization.sublime-settings"

LANGS = {
    "ZH_CN": {
        'zipfile': 'ZH_CN.zip',
        'syntax_md5sum': '44cd99cdd8ef6c2c60c0a89d53a40b95'
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
    PACKAGES_PATH = sublime.packages_path()
    DEFAULT_PATH = os.path.join(PACKAGES_PATH, "Default")
    SYN_PATH = os.path.join(DEFAULT_PATH, "Syntax.sublime-menu")

    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    LOCALZIP_PATH = os.path.join(BASE_PATH, LANGS[lang]['zipfile'])
    if os.path.isfile(SYN_PATH):
        with open(SYN_PATH, "rb") as f:
            syntax = f.read()
        m = md5()
        m.update(syntax)
        if lang and m.hexdigest() == LANGS[lang]['syntax_md5sum']:
            sublime.status_message("%s has loaded." % lang)
            return
    if not os.path.isdir(DEFAULT_PATH):
        os.mkdir(DEFAULT_PATH)
    with zipfile.ZipFile(LOCALZIP_PATH, "r") as f:
        f.extractall(DEFAULT_PATH)


class ToggleLanguageCommand(sublime_plugin.WindowCommand):

    def run(self, language):
        set_language(language)
        restore_language_setting(language)

    def is_checked(self, language):
        return get_language_setting() == language


def plugin_loaded():
    """Load and unzip the files."""
    sublime.set_timeout(init, 200)