<p align="center"><img src="http://i.imgur.com/mqWvEv1.png" style="border: 0px;"></p>

## Documentation

###### Python Scripts:

---

**unpackfiles.py**

For each subdirectory under the calling directory move the contents into the parent directory and delete the empty subdirectory.

---

**sortdownloads.py**

Searches for video files resurively in the calling directory. Any that are found matching an expected season+episode pattern are moved to the folder specified under <sortdownloads> in the config.xml. Moves files to "<sortdownloads>\Show Name\Season Number\Renamed Video File.avi" 

| argument     | shortcut | description |
|:-------------|:---------|:------|:------------|
| --keep_title  | -k  | Keep the tvshow episode title when sorting downloads. |

---

**renamefiles.py**

renames files in the calling directory based on the provided command arguments.

| long key     | short key | description |
|:-------------|:---------|:------|:------------|
| --replace_this | -r | Replace this string. |
| --with_this | -w | With this string. | 
| --repeat | -c | Repeat the operation this many times.|
| --recursive | -v | Replace filenames in root directory and all subfolders. |
| --starts_with | -s | Replace first instance if the filename starts with [--replace_this/-r] string. |
| --ends_with | -e | Replace last instance if the filename ends with [--replace_this/-r] string. |
| --preset | -p | Run the preset formatting for files. Must be the first given argument. |

### Downloads
 - version 1.0 | [(zip)](https://github.com/admiraltoad/ScotchPy/archive/1.0.zip) | [(tar.gz)](https://github.com/admiraltoad/ScotchPy/archive/1.0.tar.gz) |
