import logging

# The LogHandler class is a custom logging handler that outputs log messages to a QTextEdit widget.
# This allows logs to be displayed in a PyQt GUI application in real-time.
class LogHandler(logging.Handler):
    # Constructor: Initializes the custom logging handler with a QTextEdit widget.
    # The text_edit parameter is the QTextEdit widget where log messages will be displayed.
    def __init__(self, text_edit):
        super().__init__()  # Initialize the base logging.Handler class.
        self.text_edit = text_edit  # Store the reference to the QTextEdit widget.

    # The emit method is called whenever a log message is generated.
    # It formats the log record and appends it to the QTextEdit widget.
    def emit(self, record):
        # Format the log record into a string message.
        message = self.format(record)

        # Append the formatted log message to the QTextEdit widget.
        self.text_edit.appendPlainText(message)

        # Automatically scroll the QTextEdit widget to display the latest log message.
        self.text_edit.verticalScrollBar().setValue(
            self.text_edit.verticalScrollBar().maximum()
        )