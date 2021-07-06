import requests
import zipfile
import tempfile
import pdf_maker
import shutil
import sys
from tkinter import messagebox as mbox
from PyPDF2 import PdfFileMerger


# From guya.moe it's possible to download different kaguya manga, such as the official or the doujin.
def download_chapter(manga_to_download, chapter, path_to_download_to, wants_zip=False, loading_bar=None, app_root=None, label=None, button=None, button_vol=None):
    if path_to_download_to is "":
        print("No argument was given for path_to_download_to")
        return
    dirpath = tempfile.mkdtemp()
    print(dirpath)
    # If there is no connection, display an error
    try:
        r = requests.get("https://guya.moe/api/download_chapter/" + manga_to_download + "/" + chapter + "/", stream=True)
        file_size = r.headers.get("content-length")
    except Exception as e:
        mbox.showerror("An error occurred", "Unable to estabilish a connection, check your internet settings")
        print("Error: " + str(e))
        return

    button.config(state="disabled")
    button_vol.config(state="disabled")

    download_to = path_to_download_to if wants_zip else dirpath + "/chapter.zip"
    print(path_to_download_to)
    # Save the zip file
    with open(download_to, "wb") as file:
        if file_size is None:
            print("No file size header found, cannot display progress")
            file.write(r.content)
        else:
            downloaded_data = 0
            file_size = int(file_size)
            for data in r.iter_content(chunk_size=32768):
                downloaded_data += len(data)
                file.write(data)
                progress = int(100 * downloaded_data/file_size)
                loading_bar["value"] = progress
                label.configure(text=str(progress) + "%")
                app_root.update_idletasks()
                app_root.update()

    if not wants_zip:
        # Extract the zip file
        with zipfile.ZipFile(dirpath + "/chapter.zip", 'r') as zip_ref:
            zip_ref.extractall(dirpath)
        pdf_maker.make_pdf(dirpath, path_to_download_to)

    shutil.rmtree(dirpath)
    label.configure(text="Ready")
    loading_bar["value"] = 0
    button.config(state="normal")
    button_vol.config(state="normal")


def get_chapter_list(manga_to_download):
    # If there is no connection, display an error
    try:
        r = requests.get("https://guya.moe/api/series/" + manga_to_download + "/")
    except Exception as e:
        mbox.showerror("An error occurred", "Unable to estabilish a connection, check your internet settings")
        print("Error: " + str(e))
        sys.exit()

    element_list = r.json()

    chapters = []

    for element in element_list["chapters"].items():
        chapters.append(f"{element[0]} - {element[1]['title']}")

    return chapters


def download_volume(manga_to_download, volume, path_to_download_to, loading_bar, app_root, label, button, button_vol):
    if path_to_download_to is "":
        print("No argument was given for path_to_download_to")
        return
    dirpath = tempfile.mkdtemp()
    print(dirpath)
    button.config(state="disabled")
    button_vol.config(state="disabled")
    # If there is no connection, display an error
    try:
        merger = PdfFileMerger()
        chapter_list = get_volume_list(manga_to_download, True)[int(volume) - 1]
        for i in range(len(chapter_list)):
            r = requests.get("https://guya.moe/api/download_chapter/" + manga_to_download + "/" + chapter_list[i].replace(".", "-") + "/", stream=True)
            file_size = r.headers.get("content-length")

            with open(dirpath + "/chapter.zip", "wb") as file:
                if file_size is None:
                    print("No file size header found, cannot display progress")
                    file.write(r.content)
                else:
                    downloaded_data = 0
                    file_size = int(file_size)
                    for data in r.iter_content(chunk_size=32768):
                        downloaded_data += len(data)
                        file.write(data)
                        progress = int(100 * downloaded_data / file_size)
                        loading_bar["value"] = progress
                        label.configure(text=f"{str(progress)}% ({i + 1}/{len(chapter_list)})")
                        app_root.update_idletasks()
                        app_root.update()

            # Extract the zip file
            with zipfile.ZipFile(dirpath + "/chapter.zip", 'r') as zip_ref:
                zip_ref.extractall(dirpath)
            # Create the PDF file
            file_path = dirpath + f"/{chapter_list[i].replace('.', '-')}.pdf"
            pdf_maker.make_pdf(dirpath, file_path)
            # Append the created file to the volume
            print(f"Appended file {file_path}")
            merger.append(file_path)
    except Exception as e:
        mbox.showerror("An error occurred", "Unable to estabilish a connection, check your internet settings")
        print("Error: " + str(e))
        return

    if not path_to_download_to.endswith(".pdf"):
        path_to_download_to += ".pdf"
    '''
    Tried to make this a function in pdf_maker.py, but the pdf was sorted badly 
    (e. g. chapter 1, then 10-5, then 10 and only then 2) so I decided to append the pdf files right on when they were
    created.
    '''
    merger.write(path_to_download_to)
    merger.close()

    shutil.rmtree(dirpath)
    label.configure(text="Ready")
    loading_bar["value"] = 0
    button.config(state="normal")
    button_vol.config(state="normal")


def get_volume_list(manga_to_download, wants_chapter_list=False):
    try:
        r = requests.get("https://guya.moe/api/series/" + manga_to_download + "/")
    except Exception as e:
        mbox.showerror("An error occurred", "Unable to estabilish a connection, check your internet settings")
        print("Error: " + str(e))
        sys.exit()

    element_list = r.json()

    # This horrendous line of code gets the last chapter relased and then accesses its volume number
    num_of_volumes = int(list(element_list["chapters"].items())[-1][1]["volume"])

    if not wants_chapter_list:
        return num_of_volumes

    volumes = []
    for i in range(num_of_volumes):
        volumes.append([])

    print(len(volumes))

    for element in element_list["chapters"].items():
        volumes[int(element[1]["volume"]) - 1].append(element[0])

    return volumes


if __name__ == "__main__":
    print(get_volume_list("Kaguya-Wants-To-Be-Confessed-To"))
