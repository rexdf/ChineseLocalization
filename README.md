# Chinese-Localization
Simplified Chinese and Traditional Chinese Translation for Sublime Text 3. Support MainMenu TabMenu ContextMenu,etc

**Upgrade to sublime text 3 to have a better experience.**

### Manual Install
Clone this repository into `Sublime Text 3/Packages` using OS-appropriate location:

OSX:

    git clone -b st2 https://github.com/rexdf/ChineseLocalization.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/ChineseLocalization

Windows:

    git clone -b st2 https://github.com/rexdf/Chinese-Localization.git "%APPDATA%\Sublime Text 3\Packages\ChineseLocalization"

Linux:

    git clone -b st2 https://github.com/rexdf/Chinese-Localization.git ~/.config/sublime-text-3/Packages/ChineseLocalization

Or just download this repo as zip and unzip it to `Packages/Default`

![screenshot](https://raw.githubusercontent.com/rexdf/ChineseLocalization/readme/screenshot/SublimeChineseTranslation3.gif)


![screenshot](https://raw.githubusercontent.com/rexdf/ChineseLocalization/readme/screenshot/sublime_translation.png)

![screenshot](https://raw.githubusercontent.com/rexdf/ChineseLocalization/readme/screenshot/sublime_trans_linux.png)

### Usage

- [x] Help/Language/Simplified Chinese 简体中文
- [x] Help/Language/Traditional Chinese 正體中文
- [x] Help/Language/English


### problems
Because almost every package has a `Main.sublime-menu`, So some package name maybe override the Default one.

AFAIK, minimal manual delete including:

+ **SublimeREPL** delete caption

+ **Minify** Overwrite, but delete

+ **Tag** delete mnemonic caption

+ **Indent XML** delete caption Selection

+ **HTMLBeautify** delete caption Edit

+ **GraphvizPreview** delete caption Edit

### Author & Contributors
- [Rexdf](https://github.com/rexdf)
- [FichteFoll](https://github.com/FichteFoll)
