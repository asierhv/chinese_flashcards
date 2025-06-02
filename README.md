# Chinese Flashcards Creator

This tool allows you to create printable cut-out flashcards for learning Chinese, with support for A4 and A3 page sizes.
You can run it in a python enviroment with `reportlab` installed.

You can configure multiple parameters such as flashcard size, Chinese Hanzi characters, Pinyin, and Meaning by modifying the script `generate_flashcards.py`

You can also change the language of the meaning from one of the following table.
Make sure to change the `LANGUAGE` parameter in the script and add the correspondant `HSK{lvl}_{LANGUAGE}.txt` files in the `TXT` folder.
You can check for those files at [HSK Academy](https://hsk.academy/)
| Language (Native) | Code | English Name      |
| ----------------- | ---- | ----------------- |
| English           | `en` | English           |
| العربية           | `ar` | Arabic            |
| Deutsch           | `de` | German            |
| Ελληνικά          | `el` | Greek             |
| Español           | `es` | Spanish           |
| Français          | `fr` | French            |
| Italiano          | `it` | Italian           |
| 日本語               | `ja` | Japanese          |
| ភាសាខ្មែរ         | `km` | Khmer (Cambodian) |
| 한국어               | `ko` | Korean            |
| Português         | `pt` | Portuguese        |
| Русский           | `ru` | Russian           |
| ไทย               | `th` | Thai              |
| Tiếng Việt        | `vi` | Vietnamese        |
