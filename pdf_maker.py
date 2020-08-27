from PIL import Image
import glob


def make_pdf(temp_dir_path, path_to_save_to):
    images = []

    # Append both .jpg files and .png files to the pdf
    for file in glob.glob(temp_dir_path + "/*.jpg"):
        images.append(Image.open(file).convert("RGB"))
    for file in glob.glob(temp_dir_path + "/*.png"):
        images.append(Image.open(file).convert("RGB"))

    # Check if the path ends with .pdf; if not, add it or else Pillow will complain
    if not path_to_save_to.endswith(".pdf"):
        path_to_save_to += ".pdf"
    images[0].save(path_to_save_to, save_all=True, append_images=images[1:])
