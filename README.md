# Chinese-Localization
Chinese Translation for Sublime Text 3. Support MainMenu TabMenu ContextMenu,etc

### Manual Install
Clone this repository into `Sublime Text 3/Packages` using OS-appropriate location:

OSX:

    git clone https://github.com/rexdf/Chinese-Localization.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Chinese-Localization

Windows:

    git clone https://github.com/rexdf/Chinese-Localization.git "%APPDATA%\Sublime Text 3\Packages\Chinese-Localization"

Linux:

    git clone https://github.com/rexdf/Chinese-Localization.git ~/.config/sublime-text-3/Packages/Chinese-Localization

Or just download this repo as zip and unzip it to `Packages/Default`

![screenshot](https://raw.githubusercontent.com/rexdf/Chinese-Localization/master/screenshot/SublimeChineseTranslation.gif)


![screenshot](https://raw.githubusercontent.com/rexdf/Chinese-Localization/master/screenshot/sublime_translation.png)

![screenshot](https://raw.githubusercontent.com/rexdf/Chinese-Localization/master/screenshot/sublime_trans_linux.png)


### problems
Because almost every package has a `Main.sublime-menu`, So some package name maybe override the Default one.

AFAIK,

+ **SublimeREPL** delete caption

+ **Minify** Overwrite, but delete

+ **Tag** delete mnemonic caption

+ **Indent XML** delete caption Selection

+ **GraphvizPreview** delete caption Edit