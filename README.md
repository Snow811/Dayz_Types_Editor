# DayZ Types Editor

A GUI-based tool for editing `types.xml` and managing loot configurations in DayZ. Supports integration with `cfglimitsdefinition.xml` and `cfglimitsdefinitionuser.xml` for tag-based filtering and editing.

## 🚀 Features

- Search and filter by Name, Category, Usage, Value, or Tags
- Sortable columns with one-click sorting
- Reset Sort button to restore original order and clear sort indicators
- Map Mode toggle for Vanilla vs Namalsk logic
- Batch editing of multiple entries
- Dynamic tag handling:
  - Vanilla: uses `<usage name="..."/>` and `<value name="..."/>`
  - Namalsk: uses `<tag name="..."/>` and `<value user="TierX"/>`
- Clear Selection button to deselect all rows
- Reset Filter button to clear search and restore default field
- Save to XML with clean formatting and map-aware tag output

## 🗺️ Map Mode Support

| Mode     | Usage Tags        | Value Tags             | Tag Names         |
|----------|-------------------|------------------------|-------------------|
| Vanilla  | `<usage name="X"/>` | `<value name="X"/>`     | _(not used)_      |
| Namalsk  | _(not used)_        | `<value user="TierX"/>` | `<tag name="X"/>` |

Switch modes using the **Map Mode** dropdown in the top toolbar.

## Releases

A prebuilt Windows `.exe` version is available under the [Releases](https://github.com/Snow811/Dayz_Types_Editor/releases) section.

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
- Category dropdown is protected from accidental mouse wheel changes.
- Dialogs are scrollable and resizable for better usability on small screens.

## 💡 Tips

- Use Reset Sort to undo column sorting  
- Use Clear Selection to deselect all rows  
- Switch between Vanilla and Namalsk modes to match your map logic  
- All changes are saved in clean XML format with unused fields omitted

## License

UnLicense
