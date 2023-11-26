import os
from dotenv import load_dotenv
import tkinter as tk
from PIL import Image, ImageTk
import keyboard
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with API key from .env file
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize the main Tk window and immediately hide it 
root = tk.Tk()
root.withdraw()

# Load the logo image and keep a reference to it in the root window
original_image = Image.open('openai_logo.png')
resized_image = original_image.resize((50, 50), Image.Resampling.LANCZOS)
root.logo = ImageTk.PhotoImage(resized_image)

def get_response(message):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": message}]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

popup = None  # Global reference for the popup

def create_gui():
    global root, logo, popup

    if popup is None:
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)
        popup.wm_attributes("-topmost", True)
        popup.config(bg='white')

        window_width, window_height = 400, 200
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        popup.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        logo_label = tk.Label(popup, image=root.logo, bg='white')
        logo_label.grid(row=0, column=0, padx=10, pady=20)

        prompt_label = tk.Label(popup, text="Enter your message for ChatGPT:", font=("Arial", 12), bg='white')
        prompt_label.grid(row=0, column=1, sticky='w')

        # Attach input_entry as an attribute of popup
        popup.input_entry = tk.Entry(popup, font=("Arial", 12), width=50)
        popup.input_entry.grid(row=1, column=0, columnspan=2, padx=10)

        ok_button = tk.Button(popup, text="OK", command=lambda: submit(popup.input_entry.get()))
        ok_button.grid(row=2, column=0, columnspan=2, pady=10)

        popup.input_entry.bind("<Return>", lambda event: submit(popup.input_entry.get()))

    def submit(input_text):
        global popup
        if input_text:
            response = get_response(input_text)
            print(response)
        popup.withdraw()
    
    popup.deiconify()  # Show the popup window
    popup.focus_force()  # Force focus onto the popup window

    def set_focus():
        popup.input_entry.focus_set()  # Set focus on the input entry

    popup.after(100, set_focus)  # Set focus after a short delay

# Global flag to indicate when to open the popup
open_popup_flag = False

def on_activate():
    global open_popup_flag
    open_popup_flag = True

def open_popup_if_needed():
    global open_popup_flag
    if open_popup_flag:
        create_gui()
        open_popup_flag = False
    root.after(100, open_popup_if_needed)

root.after(100, open_popup_if_needed)

# Set the hotkey
register_word_listener = keyboard.add_hotkey('ctrl+alt+`' , lambda: on_activate())

print("Script running. Use ctrl+alt+` to activate.")

root.mainloop()