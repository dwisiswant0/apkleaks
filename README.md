## apkLeaks
[![version](https://badge.fury.io/gh/dwisiswant0%2fapkleaks.svg)](https://badge.fury.io/gh/dwisiswant0%2fapkleaks.svg)
[![contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwisiswant0/apkleaks/issues)

Scanning APK file for URIs, endpoints & secrets.

![apkleaks PoC](https://user-images.githubusercontent.com/25837540/83319953-c3996880-a26c-11ea-982c-c20a343019db.png)

---

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Version](#version)
- [Legal](#legal)
- [Credits and Thanks](#credits-and-thanks)

---

### Installation

To install **apkLeaks**, simply:

```
$ git clone https://github.com/dwisiswant0/apkleaks
```

Or download at [release](https://github.com/dwisiswant0/apkleaks/releases/) tab.

### Dependencies

Install global packages & requirements,

```
$ sudo apt-get install libssl-dev swig -y
$ sudo pip install -r requirements.txt
```

### Usage

Basically,
```
$ python apkleaks.py -f ~/path/to/file.apk
```

#### Options

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

Custom patterns can be added with the following flag `--pattern /path/to/rules.json` to provide sensitive _search rules_ in the JSON file format. For example,

```json
// rules.json
{
  "Amazon AWS Access Key ID": "AKIA[0-9A-Z]{16}",
  ...
}
```

```
$ python apkleaks.py -f /path/to/file.apk -c rules.json -o ~/Documents/apkleaks-resuts.txt
```

### Version

Current version is `v0.4.1-dev`, and still development.


### Legal

This tool can be freely copied, modified, altered, distributed without any attribution whatsoever. However, if you feel like this tool deserves an attribution, mention it. It won't hurt anybody :)

[![Twitter Follow](https://img.shields.io/twitter/follow/dwisiswant0.svg?style=social)](https://twitter.com/dwisiswant0)

Please, read the [license terms](https://github.com/dwisiswant0/apkleaks/blob/master/LICENSE). Don't worry, it can be read in less than 30 seconds, unless you have some sort of reading disability - in that case, I'm wondering why you're still reading this text. Really. Stop. Please. I mean, seriously. Why are you still reading?


### Credits and Thanks

Since this tool includes some contributions, and I'm not an asshole, I'll publically thank the following users for their help and resource:

- [@ndelphit](https://github.com/ndelphit) - for his inspiring `apkurlgrep`, that's why this tool was made.
- [@dxa4481](https://github.com/dxa4481) and y'all who contribute to `truffleHogRegexes`.
- [@GerbenJavado](https://github.com/GerbenJavado) & [@Bankde](https://github.com/Bankde) - for awesome pattern to discover URLs, endpoints & their parameters from `LinkFinder`.
- [@pxb1988](https://github.com/pxb1988) - for awesome APK dissambler `dex2jar`.
- [@ph4r05](https://github.com/ph4r05) for standalone APK parser.
