from PIL import Image
import glob
import os


def make_pdf(temp_dir_path, path_to_save_to):
    images = []

    # Append both .jpg files and .png files to the pdf
    for file in sorted(glob.glob(temp_dir_path + "/*.*")):
        print(file)
        if ".png" in file or ".jpg" in file:
            images.append(Image.open(file).convert("RGB"))
            os.remove(file)

    # Check if the path ends with .pdf; if not, add it or else Pillow will complain
    if not path_to_save_to.endswith(".pdf"):
        path_to_save_to += ".pdf"
    
    illegal_characters = "*?\"<>|"
    path_to_save_to = path_to_save_to.translate({ord(i): None for i in illegal_characters})

    images[0].save(path_to_save_to, save_all=True, append_images=images[1:])
