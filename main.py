from tkinter import *
from tkinter import font
from PIL import Image, ImageDraw, ImageFont, ImageTk
from text_generator_py import get_words


def try_again():
    try_again_button.grid_remove()
    high_score_label.grid_remove()
    current_score_label.grid_remove()
    instruction_label.grid()
    text_title_label.grid()
    get_new_text()
    default_text_box()
    text_box.bind("<FocusIn>", on_focus_in)
    screen.after_idle(lambda: text_box.focus_set())


def get_new_text():
    # Setting up the text label using PIL
    rand_text_list = get_words(num=135)
    edited_list = [word + "\n" if (i + 1) % 12 == 0 else word for i, word in enumerate(rand_text_list)]
    rand_text = " ".join(edited_list)
    image_width, image_height = 1200, 400
    libre_franklin_font = ImageFont.truetype("fonts/Libre_Franklin/static/LibreFranklin-Regular.ttf", 24)
    image = Image.new("RGB", (image_width, image_height), "#D9ABAB")
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), rand_text, font=libre_franklin_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_width - text_width) / 2  # Calculate centered position
    y = (image_height - text_height) / 2
    draw.text((x, y), text=rand_text, font=libre_franklin_font, fill=(0, 0, 0))
    text_label_image = ImageTk.PhotoImage(image)
    text_label.image = text_label_image
    text_label.config(image=text_label_image)
    text_label.grid(row=2, column=1)


def default_text_box():
    text_box.delete("1.0", "end")
    text_box.tag_configure("placeholder", font=CUSTOM_FONT, foreground="#a9a9a9")  # Adding a placeholder
    text_box.insert("1.0", "Start Typing...", "placeholder")
    # Bind the all the different events to the Text box
    text_box.bind("<FocusIn>", on_focus_in)
    text_box.bind("<FocusOut>", on_focus_out)
    text_box.bind("<Key>", start_timer)
    text_box.grid(row=3, column=1, pady=10)


# ---------------------------- SCORE KEEPING FUNCTIONS ------------------------------- #
def end_time():
    print("Time Has Ended.")
    users_text = text_box.get("1.0", "end-1c")
    users_text_words = users_text.split()
    score = len(users_text_words)
    text_title_label.grid_remove() # Hides all irrelevant widgets
    text_box.grid_remove()
    text_label.grid_remove()
    instruction_label.grid_remove()
    # Updating the title label to display the score, with a new image.
    lora_font_bold = ImageFont.truetype("fonts/lora/static/Lora-Bold.ttf", 82)
    image = Image.new("RGB", (1000, 175), "#D9ABAB")
    draw = ImageDraw.Draw(image)
    draw.text((40, 40), f"Your Score Is: {score} WPM.", font=lora_font_bold, fill=(0, 0, 0))
    score_image = ImageTk.PhotoImage(image)
    current_score_label.config(image=score_image)
    current_score_label.score_image = score_image
    current_score_label.grid(row=1, column=1)

    def update_high_score(is_new, high_score):
        high_score_text = f"Your Current High Score Is:  {high_score}."
        if is_new:
            high_score_text = f"Congratulations! You Have Broke your High score!\n\nCurrent High Score Is:  {high_score}."
        libre_franklin_semi_bold_font = ImageFont.truetype("fonts/Libre_Franklin/static/LibreFranklin-SemiBold.ttf", 32)
        image = Image.new("RGB", (1000, 130), "#C75B7A")
        draw = ImageDraw.Draw(image)
        draw.text((20, 10), text=high_score_text, font=libre_franklin_semi_bold_font, fill=(255, 255, 255))
        high_score_image = ImageTk.PhotoImage(image)
        high_score_label.config(image=high_score_image)
        high_score_label.high_score_image = high_score_image
        high_score_label.grid(row=2, column=1, pady=15)

    def check_high_score(new_score):
        with open("High-score.txt", "r+") as file:
            current = int(file.read().strip())
            if current > new_score:
                update_high_score(False, current)
            else:
                file.seek(0)
                file.write(str(new_score))
                update_high_score(True, new_score)

    check_high_score(score)
    try_again_button.grid(row=3, column=1, pady=40)


# ---------------------------- TEXT BOX FUNCTIONS ------------------------------- #
def on_focus_in(event):
    text_box.delete("1.0", "end")
    text_box.unbind("<FocusIn>")


def on_focus_out(event):
    if not text_box.get("1.0", "end-1c").strip():  # Check if the text box is empty
        text_box.insert("1.0", "Start Typing...", "placeholder")


def start_timer(event):
    screen.after(3000, end_time)
    text_box.unbind("<Key>")
    print("Started Timer...")


# ---------------------------- UI SETUP ------------------------------- #
screen = Tk()
screen.title("Typing Speed Test")
screen.config(height=1800, width=3200, padx=75, pady=45, bg="#F4D9D0")
CUSTOM_FONT = font.Font(family="Arial", size=15, weight="normal")

instruction_label = Label(screen, text="This is a typing speed test. A 60 second timer will begin when you'll start "
                                       "typing. Good luck!", font=CUSTOM_FONT, bg="#F4D9D0", highlightthickness=0,
                                       borderwidth=0, anchor="center", justify="center")
instruction_label.grid(row=0, column=1)

# Setting up the title label using PIL, creating a custom font
lora_font = ImageFont.truetype("fonts/lora/static/Lora-Regular.ttf", 60)
image = Image.new("RGB", (400, 110), "#F4D9D0")
draw = ImageDraw.Draw(image)
draw.text((10, 25), "Start Typing:", font=lora_font, fill=(0, 0, 0))  # Black text
title_label_image = ImageTk.PhotoImage(image)
text_title_label = Label(screen, image=title_label_image, highlightthickness=0, borderwidth=0, anchor="center")
text_title_label.grid(row=1, column=1)

# Setting up the random text label
text_label = Label(screen, highlightthickness=0, borderwidth=0)
get_new_text()

# Setting up a text box
text_box = Text(screen, width=109, height=11, highlightthickness=0, borderwidth=0, font=CUSTOM_FONT)
default_text_box()

# Setting the different score widgets
current_score_label = Label(screen, highlightthickness=0, borderwidth=0)
high_score_label = Label(screen, highlightthickness=0, borderwidth=0)
try_again_button = Button(screen, text="Try Again", bg="#921A40", fg="white", font=CUSTOM_FONT, width=20, height=1,
                          borderwidth=4, highlightthickness=4, highlightbackground="white", pady=5, command=try_again)

screen.mainloop()
