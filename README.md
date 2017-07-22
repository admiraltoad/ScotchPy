<p align="center"><img src="http://i.imgur.com/mqWvEv1.png" style="border: 0px;"></p>

## Documentation

**unpackfiles.py**

For each subdirectory under the calling directory move the contents into the parent directory and delete the empty subdirectory.

---

**sortdownloads.py**

Searches for video files resurively in the calling directory. Any that are found matching an expected season+episode pattern are moved to the folder specified under <sortdownloads> in the config.xml. Moves files to "<sortdownloads>\Show Name\Season Number\Renamed Video File.avi" 

<table>
<tr>
<th style="width:25%">argument</th>
<th style="width:10%">short key</th>
<th style="width:65%">description</th>
</tr>
<tr>
<td>--keep_title</td>
<td>-k</td>
<td>Keep the tvshow episode title when sorting downloads.</td>
</tr>
</table>

---

**renamefiles.py**

renames files in the calling directory based on the provided command arguments.

<table>
<tr>
<th style="width:25%">argument</th>
<th style="width:10%">short key</th>
<th style="width:65%">description</th>
</tr>
<tr><td>--replace_this</td><td>-r</td><td>Replace this string.</td></tr>
<tr><td>--with_this</td><td>-w</td><td>With this string. </td></tr>
<tr><td>--repeat</td><td>-c</td><td>Repeat this many times.</td></tr>
<tr><td>--recursive</td><td>-v</td><td>Replace in calling directory recursively.</td></tr>
<tr><td>--starts_with</td><td>-s</td><td>Replace if the filename starts with [--replace_this/-r] string.</td></tr>
<tr><td>--ends_with</td><td>-e</td><td>Replace if the filename ends with [--replace_this/-r] string.</td></tr>
<tr><td>--preset</td><td>-p</td><td>Run the preset formatting for files. Must be the first given argument.</td></tr>
</table>

### Downloads
 - version 1.0 | [(zip)](https://github.com/admiraltoad/ScotchPy/archive/1.0.zip) | [(tar.gz)](https://github.com/admiraltoad/ScotchPy/archive/1.0.tar.gz) |
