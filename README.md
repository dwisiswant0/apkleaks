# APKLeaks
[![version](https://badge.fury.io/gh/dwisiswant0%2fapkleaks.svg)](https://badge.fury.io/gh/dwisiswant0%2fapkleaks.svg)
[![contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwisiswant0/apkleaks/issues)

Scanning APK file for URIs, endpoints & secrets.

![apkleaks PoC](https://user-images.githubusercontent.com/25837540/109804969-7613b700-7c55-11eb-8f6c-bacce0d1250e.png)

---

- [Installation](#installation)
- [Usage](#usage)
- [Version](#version)
- [Legal](#legal)
- [Acknowledments](#credits-and-thanks)

---

## Installation

To install **apkLeaks**, simply:

```
$ git clone https://github.com/dwisiswant0/apkleaks
$ cd apkleaks/
$ pip install -r requirements.txt
```

## Usage

It's fairly simple,
```
$ python apkleaks.py -f ~/path/to/file.apk
```

### Options

```
usage: apkleaks [-h] -f FILE [-o OUTPUT] [-p PATTERN]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  APK file to scanning
  -o OUTPUT, --output OUTPUT
                        Write to file results (NULL will be saved into random
                        file)
  -p PATTERN, --pattern PATTERN
                        Path to custom patterns JSON
```

In general, if you don't provide `-o` argument, then it will generate results file automatically.

Custom patterns can be added with the following flag `--pattern /path/to/rules.json` to provide sensitive _search rules_ in the JSON file format. If not set, it'll use default patterns from [regexes.json](https://github.com/dwisiswant0/apkleaks/blob/dev/config/regexes.json) file.

Example patterns file:

```json
// rules.json
{
  "Amazon AWS Access Key ID": "AKIA[0-9A-Z]{16}",
  ...
}
```

```
$ python apkleaks.py -f /path/to/file.apk -p rules.json -o ~/Documents/apkleaks-resuts.txt
```

## Version

Current version is `v2.0.1`, and still development.

## Legal

`apkleaks` is distributed under Apache 2.

## Acknowledments

Since this tool includes some contributions, and I'm not an asshole, I'll publically thank the following users for their helps and resources:

- [@ndelphit](https://github.com/ndelphit) - for his inspiring `apkurlgrep`, that's why this tool was made.
- [@dxa4481](https://github.com/dxa4481) and y'all who contribute to `truffleHogRegexes`.
- [@GerbenJavado](https://github.com/GerbenJavado) & [@Bankde](https://github.com/Bankde) - for awesome pattern to discover URLs, endpoints & their parameters from `LinkFinder`.
- [@tomnomnom](https://github.com/tomnomnom/gf) - a `gf` patterns.
- [@pxb1988](https://github.com/pxb1988) - for awesome APK dissambler `dex2jar`.
- [@subho007](https://github.com/ph4r05) for standalone APK parser.
- `SHA2048#4361` _(Discord user)_ that help me porting code to Python3.