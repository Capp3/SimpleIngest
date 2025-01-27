import logging

class LogHandler(logging.Handler):
    """Custom logging handler to output logs to a QTextEdit."""
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        message = self.format(record)
        self.text_edit.appendPlainText(message)
        self.text_edit.verticalScrollBar().setValue(
            self.text_edit.verticalScrollBar().maximum()
        )