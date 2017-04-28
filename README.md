# Chinese Localization
Simplified Chinese and Traditional Chinese Translation for Sublime Text 3. Support MainMenu TabMenu ContextMenu,etc.

I try to support more languages. Now Japanese is partially supported.

### Manual Install
Clone this repository into `Sublime Text 3/Packages` using OS-appropriate location:

OSX:

    git clone -b st3 https://github.com/rexdf/ChineseLocalization.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/ChineseLocalization

Windows:

    git clone -b st3 https://github.com/rexdf/ChineseLocalization.git "%APPDATA%\Sublime Text 3\Packages\ChineseLocalization"

Linux:

    git clone -b st3 https://github.com/rexdf/ChineseLocalization.git ~/.config/sublime-text-3/Packages/ChineseLocalization

~~Or just download this repo as zip, rename it to `ChineseLocalization.sublime-package` and put it to `Data\Installed Packages`. (Sublime Text 3 only)~~ You need to unpack and pack it again to make sure all files in the zip root rather than `ChineseLocalization-st3` folder.

**Recommand for 3124+, click Menu `Tools\Install Package Control` , then Menu `Preferences\Package Control ` , install `Chinese​Localizations`.**


![screenshot](https://raw.githubusercontent.com/rexdf/ChineseLocalization/readme/screenshot/SublimeChineseTranslation3.gif)


![screenshot](https://raw.githubusercontent.com/rexdf/ChineseLocalization/readme/screenshot/sublime_translation.png)

![screenshot](https://raw.githubusercontent.com/rexdf/ChineseLocalization/readme/screenshot/sublime_trans_linux.png)

### Usage

- [x] Help/Language/Simplified Chinese 简体中文
- [x] Help/Language/Traditional Chinese 正體中文
- [ ] Help/Language/Japanese 日本語
- [x] Help/Language/English


### problems

Now this problem has been solved at st3-1.6.0.

~~Because almost every package has a `Main.sublime-menu`, So some package name maybe override the Default one.~~

~~AFAIK, minimal manual delete including~~:

+ **SublimeREPL** delete caption

+ **Minify** Overwrite, but delete

+ **Tag** delete mnemonic caption

+ **Indent XML** delete caption Selection

+ **HTMLBeautify** delete caption Edit

+ **GraphvizPreview** delete caption Edit

### Author & Contributors
- [Rexdf](https://github.com/rexdf)
- [FichteFoll](https://github.com/FichteFoll)
- [Patrick T.](https://github.com/Patricivs)
