from PyQt5.QtWidgets import QApplication
from editor import TypesEditor
import sys

def apply_dark_theme(app):
    dark_stylesheet = """
    QWidget {
        background-color: #2b2b2b;
        color: #f0f0f0;
        font-family: Segoe UI, sans-serif;
        font-size: 10pt;
    }
    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QListWidget, QTableWidget {
        background-color: #3c3f41;
        color: #f0f0f0;
        border: 1px solid #555;
    }
    QPushButton {
        background-color: #555;
        border: 1px solid #777;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #666;
    }
    QHeaderView::section {
        background-color: #444;
        color: #f0f0f0;
        padding: 4px;
        border: 1px solid #666;
    }
    QTableWidget::item:selected {
        background-color: #607d8b;
        color: white;
    }
    QScrollBar:vertical, QScrollBar:horizontal {
        background: #2b2b2b;
        width: 12px;
    }
    QScrollBar::handle {
        background: #555;
        border-radius: 6px;
    }
    QScrollBar::handle:hover {
        background: #777;
    }
    """
    app.setStyleSheet(dark_stylesheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    editor = TypesEditor()
    editor.show()
    sys.exit(app.exec_())
