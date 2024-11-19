from shiny import App, ui, reactive, render
from cryptography.fernet import Fernet

# Generate a key (only once, store it securely)
key = Fernet.generate_key()
cipher = Fernet(key)

app_ui = ui.page_fluid(
    ui.h2("Python Shiny App with Cryptography"),
    ui.input_text("text_to_encrypt", "Enter text to encrypt:", ""),
    ui.output_text_verbatim("encrypted_text"),
    ui.input_text("text_to_decrypt", "Enter encrypted text to decrypt:", ""),
    ui.output_text_verbatim("decrypted_text"),
)

def server(input, output, session):
    @output
    @render.text
    def encrypted_text():
        text = input.text_to_encrypt()
        if text:
            return cipher.encrypt(text.encode()).decode()
        return "Enter text to see encryption."

    @output
    @render.text
    def decrypted_text():
        encrypted = input.text_to_decrypt()
        if encrypted:
            try:
                return cipher.decrypt(encrypted.encode()).decode()
            except Exception:
                return "Decryption failed. Ensure the text was encrypted using this app."
        return "Enter encrypted text to see decryption."

app = App(app_ui, server)
