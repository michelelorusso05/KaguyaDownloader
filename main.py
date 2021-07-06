# System Libraries
import os
import sys
import webbrowser
from tkinter import ttk
from tkinter import filedialog
from tkinter import IntVar, PhotoImage
from ttkthemes import themed_tk as tk

# Custom Libraries
import chapter_downloader

manga_names = ["Kaguya-Wants-To-Be-Confessed-To",
               "We-Want-To-Talk-About-Kaguya",
               "Kaguya-Wants-To-Be-Confessed-To-Official-Doujin"]

choices = [chapter_downloader.get_chapter_list("Kaguya-Wants-To-Be-Confessed-To"),
           chapter_downloader.get_chapter_list("We-Want-To-Talk-About-Kaguya"),
           chapter_downloader.get_chapter_list("Kaguya-Wants-To-Be-Confessed-To-Official-Doujin")]

choices_vol = [[f"Volume {j + 1}" for j in range(chapter_downloader.get_volume_list(manga_names[i]))] for i in range(len(manga_names))]

volume_list_official = [f"Volume {i + 1}" for i in range(chapter_downloader.get_volume_list("Kaguya-Wants-To-Be-Confessed-To"))]
volume_list_spinoff = [f"Volume {i + 1}" for i in range(chapter_downloader.get_volume_list("We-Want-To-Talk-About-Kaguya"))]
volume_list_doujin = [f"Volume {i + 1}" for i in range(chapter_downloader.get_volume_list("Kaguya-Wants-To-Be-Confessed-To-Official-Doujin"))]

app = tk.ThemedTk()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def download():
    if note_book.index("current") == 0:

        filepath = dropDown.get()
        illegal_characters = ":*?\"<>|"
        filepath = filepath.translate({ord(i): None for i in illegal_characters})

        if wants_zip.get() == 0:
            download_path = filedialog.asksaveasfilename(initialdir="/",
                                                         initialfile=filepath + ".pdf",
                                                         title="Select where to save the downloaded chapter",
                                                         filetypes=(
                                                                ("PDF documents", "*.pdf"),
                                                                )
                                                         )
        else:
            download_path = filedialog.asksaveasfilename(initialdir="/",
                                         initialfile=filepath + ".zip",
                                         title="Select where to save the downloaded chapter",
                                         filetypes=(
                                             ("Compressed files", "*.zip"),
                                             )
                                         )
        chapter_downloader.download_chapter(manga_names[selected_manga.get()], selected_chapter, download_path,
                                            bool(wants_zip.get()), progress, app, progressLabel, button, button_vol)
    elif note_book.index("current") == 1:

        filepath = dropDown_vol.get()
        illegal_characters = "*?\"<>|"
        filepath = filepath.translate({ord(i): None for i in illegal_characters})

        download_path = filedialog.asksaveasfilename(initialdir="/",
                                                     initialfile=filepath + ".pdf",
                                                     title="Select where to save the downloaded volume",
                                                     filetypes=(
                                                         ("PDF documents", "*.pdf"),
                                                     )
                                                     )
        chapter_downloader.download_volume(manga_names[selected_manga.get()], filepath.replace("Volume ", ""),
                                           download_path, progress, app, progressLabel, button, button_vol)


app.title("Kaguya Downloader")
app.resizable(0, 0)

app.get_themes()
app.set_theme("breeze")

try:
	app.iconphoto(True, PhotoImage(file=resource_path("logo.png")))
except:
	print("Unable to find logo.png, enjoy Kaguya Downloader without the icon ;(")

note_book = ttk.Notebook(app)
page_download_chapters = ttk.Frame(note_book)
page_download_volumes = ttk.Frame(note_book)
page_show_help = ttk.Frame(note_book)

selected_manga = IntVar()
selected_manga.set(0)

wants_zip = IntVar()
wants_zip.set(0)

selected_chapter = "1"

# Single Chapter Download

labelTop = ttk.Label(page_download_chapters, text="Chapter to download:")
labelTop.grid(column=0, row=0)

dropDown = ttk.Combobox(page_download_chapters, values=choices[selected_manga.get()], state="readonly", width=75)

dropDown.grid(column=0, row=1, padx=10, pady=10)
dropDown.current(0)

button = ttk.Button(page_download_chapters, text="Download selected chapter", command=download)
button.grid(column=0, row=2)


r1 = ttk.Radiobutton(page_download_chapters, text="Kaguya wants to be confessed to", variable=selected_manga, value=0)
r1.grid(column=1, row=0, sticky="W", pady=(10, 0))
r2 = ttk.Radiobutton(page_download_chapters, text="We want to talk about Kaguya [SPINOFF]", variable=selected_manga, value=1)
r2.grid(column=1, row=1, sticky="W")
r3 = ttk.Radiobutton(page_download_chapters, text="Kaguya wants to be confessed to [DOUJIN]", variable=selected_manga, value=2)
r3.grid(column=1, row=2, sticky="W")

btn_zip_download = ttk.Checkbutton(page_download_chapters, text="Download raw zip instead of creating a PDF file",
                                   var=wants_zip, onvalue=1, offvalue=0)

btn_zip_download.grid(column=1, row=4, pady=(20, 0))

# Volume Download

labelTop_vol = ttk.Label(page_download_volumes, text="Volume to download:")
labelTop_vol.grid(column=0, row=0)

dropDown_vol = ttk.Combobox(page_download_volumes, values=choices_vol[selected_manga.get()], state="readonly", width=75)

dropDown_vol.grid(column=0, row=1, padx=10, pady=10)
dropDown_vol.current(0)

button_vol = ttk.Button(page_download_volumes, text="Download selected volume", command=download)
button_vol.grid(column=0, row=2)


r1_vol = ttk.Radiobutton(page_download_volumes, text="Kaguya wants to be confessed to", variable=selected_manga, value=0)
r1_vol.grid(column=1, row=0, sticky="W", pady=(10, 0))
r2_vol = ttk.Radiobutton(page_download_volumes, text="We want to talk about Kaguya [SPINOFF]", variable=selected_manga, value=1)
r2_vol.grid(column=1, row=1, sticky="W")
r3_vol = ttk.Radiobutton(page_download_volumes, text="Kaguya wants to be confessed to [DOUJIN]", variable=selected_manga, value=2)
r3_vol.grid(column=1, row=2, sticky="W")

# Info Section

info_title = ttk.Label(page_show_help, text="Kaguya Downloader", font=("Arial", 20))
info_title.pack(pady=10)
info_version = ttk.Label(page_show_help, text="Ver. 1.1", font=("Arial", 10))
info_version.pack(pady=5)
info_author = ttk.Label(page_show_help, text="Created by u/MikBros", font=("Arial", 10))
info_author.pack(pady=5)
report_bug = ttk.Button(page_show_help, text="Report a bug", command=lambda: (webbrowser.open("https://www.reddit.com/message/compose/?to=MikBros")))
report_bug.pack(pady=10)


def on_value_change(event):
    global selected_chapter
    # The extra chapters have urls that contain dashes instead of dots (e. g. 64.5 becomes 64-5)
    selected_chapter = ((dropDown.get()).split(" ", 1)[0]).replace(".", "-")


def on_radiobutton_change(a, b, c):
    dropDown.config(values=choices[selected_manga.get()])
    dropDown_vol.config(values=choices_vol[selected_manga.get()])
    dropDown.current(0)
    dropDown_vol.current(0)


dropDown.bind("<<ComboboxSelected>>", on_value_change)
selected_manga.trace_add("write", on_radiobutton_change)

note_book.add(page_download_chapters, text="Chapters")
note_book.add(page_download_volumes, text="Volumes")
note_book.add(page_show_help, text="Info")

note_book.grid(column=0, row=0, padx=10, pady=10, ipadx=10, ipady=10)

progress = ttk.Progressbar(app, orient="horizontal", length=450, mode='determinate')
progress.grid(column=0, row=2, ipady=5)

progressLabel = ttk.Label(app, text="Ready")
progressLabel.grid(column=0, row=1, pady=(5, 0))


app.mainloop()
