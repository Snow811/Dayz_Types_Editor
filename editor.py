from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QApplication,
    QDialog, QMessageBox, QCheckBox, QComboBox, QGridLayout
)
from PyQt5.QtCore import Qt
from types_parser import load_types, save_types
from limits_parser import build_tag_config
from config_manager import save_config, load_config

class TypesEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DayZ Types Editor")
        self.resize(1400, 600)

        self.items = []
        self.tree_obj = None
        self.types_path = ""
        self.tag_config = {
            "usage": [], "value": [],
            "categories": [], "tags": [],
            "usage_aliases": {}, "value_aliases": {}
        }

        self.init_ui()

        def_path, user_path = load_config()
        if def_path and user_path:
            try:
                self.tag_config = build_tag_config(def_path, user_path)
                print(f"Auto-loaded limits configs:\n  {def_path}\n  {user_path}")
            except Exception as e:
                print(f"Failed to auto-load limits configs: {e}")

    def init_ui(self):
        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Name", "Nominal", "Lifetime", "Restock", "Min", "QuantMin", "QuantMax", "Cost", "Usage", "Value"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.edit_selected)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Load Types File")
        load_btn.clicked.connect(self.load_types_file)
        btn_layout.addWidget(load_btn)

        config_btn = QPushButton("Load Limits Configs")
        config_btn.clicked.connect(self.load_limits_files)
        btn_layout.addWidget(config_btn)

        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(lambda: self.edit_selected())
        btn_layout.addWidget(edit_btn)

        save_btn = QPushButton("Save Types File")
        save_btn.clicked.connect(self.save_types_file)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def load_types_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select types.xml", "", "XML Files (*.xml)")
        if not path:
            return
        try:
            self.items, self.tree_obj = load_types(path)
            self.types_path = path
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load types file:\n{str(e)}")

    def load_limits_files(self):
        def_path, _ = QFileDialog.getOpenFileName(self, "Select cfglimitsdefinition.xml", "", "XML Files (*.xml)")
        user_path, _ = QFileDialog.getOpenFileName(self, "Select cfglimitsdefinitionuser.xml", "", "XML Files (*.xml)")
        if def_path and user_path:
            self.tag_config = build_tag_config(def_path, user_path)
            save_config(def_path, user_path)
            QMessageBox.information(self, "Config Loaded", "Limits definitions loaded and saved.")

    def refresh_table(self):
        self.table.setRowCount(0)
        for item in self.items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["nominal"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["lifetime"]))
            self.table.setItem(row, 3, QTableWidgetItem(item["restock"]))
            self.table.setItem(row, 4, QTableWidgetItem(item["min"]))
            self.table.setItem(row, 5, QTableWidgetItem(item["quantmin"]))
            self.table.setItem(row, 6, QTableWidgetItem(item["quantmax"]))
            self.table.setItem(row, 7, QTableWidgetItem(item["cost"]))
            self.table.setItem(row, 8, QTableWidgetItem(", ".join(item["usage"])))
            self.table.setItem(row, 9, QTableWidgetItem(", ".join(item["value"])))

    def filter_table(self):
        text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            item_name = self.table.item(row, 0).text().lower()
            self.table.setRowHidden(row, text not in item_name)

    def edit_selected(self, row=None, column=None):
        selected = row if row is not None else self.table.currentRow()
        if selected < 0 or selected >= len(self.items):
            return
        item = self.items[selected]

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit: {item['name']}")
        dialog.resize(600, 800)
        layout = QVBoxLayout(dialog)

        def make_field(label, key):
            layout.addWidget(QLabel(label))
            field = QLineEdit(item[key])
            layout.addWidget(field)
            return field

        nominal_field = make_field("Nominal", "nominal")
        lifetime_field = make_field("Lifetime", "lifetime")
        restock_field = make_field("Restock", "restock")
        min_field = make_field("Min", "min")
        quantmin_field = make_field("QuantMin", "quantmin")
        quantmax_field = make_field("QuantMax", "quantmax")
        cost_field = make_field("Cost", "cost")

        layout.addWidget(QLabel("Flags"))
        flags_grid = QGridLayout()
        flag_fields = {}
        for i, flag in enumerate(["count_in_cargo", "count_in_hoarder", "count_in_map", "count_in_player", "crafted", "deloot"]):
            cb = QCheckBox(flag)
            cb.setChecked(item["flags"].get(flag, "0") == "1")
            flags_grid.addWidget(cb, i // 2, i % 2)
            flag_fields[flag] = cb
        layout.addLayout(flags_grid)

        layout.addWidget(QLabel("Category"))
        category_field = QComboBox()
        category_field.addItems(self.tag_config.get("categories", []))
        category_field.setEditable(True)
        category_field.setCurrentText(item["category"])
        layout.addWidget(category_field)

        def make_multiselect_grid(label, options, selected):
            layout.addWidget(QLabel(label))
            grid = QGridLayout()
            checkbox_dict = {}
            cols = 3
            for i, opt in enumerate(options):
                cb = QCheckBox(opt)
                cb.setChecked(opt in selected)
                grid.addWidget(cb, i // cols, i % cols)
                checkbox_dict[opt] = cb
            layout.addLayout(grid)
            return checkbox_dict

        usage_checks = make_multiselect_grid("Usage Tags", self.tag_config.get("usage", []), item["usage"])
        value_checks = make_multiselect_grid("Value Tags", self.tag_config.get("value", []), item["value"])
        tag_checks = make_multiselect_grid("Tag Names", self.tag_config.get("tags", []), item["tags"])

        def apply_changes():
            item["nominal"] = nominal_field.text()
            item["lifetime"] = lifetime_field.text()
            item["restock"] = restock_field.text()
            item["min"] = min_field.text()
            item["quantmin"] = quantmin_field.text()
            item["quantmax"] = quantmax_field.text()
            item["cost"] = cost_field.text()
            item["flags"] = {flag: "1" if cb.isChecked() else "0" for flag, cb in flag_fields.items()}
            item["category"] = category_field.currentText()
            item["usage"] = [tag for tag, cb in usage_checks.items() if cb.isChecked()]
            item["value"] = [tag for tag, cb in value_checks.items() if cb.isChecked()]
            item["tags"] = [tag for tag, cb in tag_checks.items() if cb.isChecked()]
            self.refresh_table()
            dialog.accept()

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(apply_changes)
        layout.addWidget(apply_btn)

        dialog.exec_()

    def save_types_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save types.xml", "types_updated.xml", "XML Files (*.xml)")
        if path:
            save_types(self.items, self.tree_obj, path)
            QMessageBox.information(self, "Saved", f"File saved to {path}")
