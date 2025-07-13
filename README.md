# DayZ Types Editor

A GUI-based tool for editing `types.xml` and managing loot configurations in DayZ. Supports integration with `cfglimitsdefinition.xml` and `cfglimitsdefinitionuser.xml` for tag-based filtering and editing.

## Features

- Load and edit `types.xml` entries
- View and modify loot parameters: `nominal`, `lifetime`, `restock`, `min`, `quantmin`, `quantmax`, `cost`
- Edit flags, category, usage tags, value tags, and tag names
- Auto-load limits config files on startup
- Double-click table entries to open the edit dialog
- Save updated `types.xml` with clean formatting and correct values

## Releases

A prebuilt Windows `.exe` version is available under the [Releases](https://github.com/your-repo/releases) section.

### How to Use

1. Download the latest `.zip` from the Releases page.
2. Extract the contents to any folder.
3. Run `DayZTypesEditor.exe`.
4. Use the GUI to load and edit your `types.xml` and limits config files.

> No Python installation required. All dependencies are bundled in the executable.

## Requirements (for source version)

- Python 3.8+
- `PyQt5`
- `lxml`

Install dependencies:

```bash
pip install PyQt5 lxml
```

## Usage (source version)

1. Run the application:

```bash
python main.py
```

2. Load your `types.xml` file using the "Load Types File" button.

3. (Optional) Load `cfglimitsdefinition.xml` and `cfglimitsdefinitionuser.xml` using the "Load Limits Configs" button. These paths will be saved and auto-loaded next time.

4. Use the search bar to filter entries.

5. Double-click any row or use "Edit Selected" to modify an entry.

6. Click "Apply" to save changes to memory.

7. Use "Save Types File" to export the updated `types.xml`.

## File Structure

- `main.py`: Launches the GUI
- `editor.py`: Main interface logic
- `types_parser.py`: XML load/save for `types.xml`
- `limits_parser.py`: Tag config loader
- `config_manager.py`: Stores config paths in `config.json`

## Notes

- The tool preserves all field values and writes clean XML using `lxml`.
- Self-closing tags are avoided; all loot parameters are saved as value tags.
- Limits config files are optional but recommended for tag filtering.

## License

MIT License
