import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QComboBox, QTextEdit,
    QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt


class JSONMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Maker")
        self.setFixedSize(700, 500)

        self.data = {}

        layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter key name")

        self.value_input = QLineEdit()
   
        self.value_input.setPlaceholderText("Enter value")

        self.type_selector = QComboBox()
        self.type_selector.addItems(["string", "number", "boolean"])

        add_btn = QPushButton("Add Key")
        add_btn.clicked.connect(self.add_key)

        input_layout.addWidget(QLabel("Key:"))
        input_layout.addWidget(self.key_input)
        input_layout.addWidget(QLabel("Value:"))
        input_layout.addWidget(self.value_input)
        input_layout.addWidget(QLabel("Type:"))
        input_layout.addWidget(self.type_selector)
        input_layout.addWidget(add_btn)

        self.json_preview = QTextEdit()
        self.json_preview.setReadOnly(True)
        self.json_preview.setStyleSheet("background: #1e1e1e; color: #00ffcc; font-family: Consolas;")

        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save JSON")
        save_btn.clicked.connect(self.save_json)
        load_btn = QPushButton("📂 Load JSON")
        load_btn.clicked.connect(self.load_json)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(load_btn)

        layout.addLayout(input_layout)
        layout.addWidget(QLabel("Live JSON Preview:"))
        layout.addWidget(self.json_preview)
        layout.addLayout(button_layout)

    def add_key(self):
        """Add key/value to dictionary and refresh preview."""
        key = self.key_input.text().strip()
        value = self.value_input.text().strip()
        vtype = self.type_selector.currentText()

        if not key:
            QMessageBox.warning(self, "Error", "Key cannot be empty!")
            return

        if vtype == "number":
            try:
                value = int(value) if value.isdigit() else float(value)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid number format!")
                return
        elif vtype == "boolean":
            if value.lower() in ["true", "yes", "1"]:
                value = True
            elif value.lower() in ["false", "no", "0"]:
                value = False
            else:
                QMessageBox.warning(self, "Error", "Boolean must be True/False")
                return

        self.data[key] = value
        self.update_preview()

        self.key_input.clear()
        self.value_input.clear()

    def update_preview(self):
        """Update the JSON preview box."""
        formatted = json.dumps(self.data, indent=4)
        self.json_preview.setPlainText(formatted)

    def save_json(self):
        """Save current JSON to file."""
        path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            QMessageBox.information(self, "Saved", f"JSON saved to {path}")

    def load_json(self):
        """Load JSON from file."""
        path, _ = QFileDialog.getOpenFileName(self, "Open JSON", "", "JSON Files (*.json)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                self.update_preview()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load JSON:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JSONMaker()
    window.show()
    sys.exit(app.exec())
