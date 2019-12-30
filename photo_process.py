import hashlib
from glob import glob
import os
from PIL import Image, ExifTags
from datetime import datetime
import exifread
from time import sleep


def photo_rename_date(main_dir):
    """
    Rename files based on datetime created
    """

    for f_dir, _, _ in os.walk(main_dir):
        print(f_dir)
        for f in glob(f_dir + "/*.*"):

            f_ext = "." + os.path.basename(f).split(".")[-1]

            # Extract datetime of file creation
            try:
                if f_ext.lower() in (".jpg", ".jpeg", ".png"):
                    img = Image.open(f)
                    exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}

                    if 'DateTime' in exif:
                        d = datetime.strptime(exif['DateTime'], "%Y:%m:%d %H:%M:%S")
                    elif 'DateTimeOriginal' in exif:
                        d = datetime.strptime(exif['DateTimeOriginal'], "%Y:%m:%d %H:%M:%S")
                    else:
                        pass
                    img.close()

                elif f_ext.lower() in (".tif", ".tiff"):
                    with open(f, 'rb') as img:
                        tags = exifread.process_file(img)
                    d = datetime.strptime(tags['EXIF DateTimeDigitized'].printable, "%Y:%m:%d %H:%M:%S")

            except:
                d = datetime.utcfromtimestamp(os.path.getmtime(f))
                try:
                    img.close()
                except:
                    pass

            # t = os.path.getctime(f)
            # d = datetime.utcfromtimestamp(t) - timedelta(hours=6)

            # Convert datetime into string format
            f_name = d.strftime("%Y-%m-%d %H%M%S")

            # If filename already correct, skip, otherwise rename
            if f_name == ".".join(os.path.basename(f).split(".")[:-1]):
                continue

            # Get file extension
            f_ext = "." + os.path.basename(f).split(".")[-1]

            # Rename file including possible number expansion
            tmp_f_name = f_name
            counter = 1
            while os.path.isfile(f_dir + "/" + tmp_f_name + f_ext):
                tmp_f_name = f_name + "-{:d}".format(counter)
                sleep(1)
                counter += 1

            os.rename(f, f_dir + "/" + tmp_f_name + f_ext)
            print("\tRenaming {} to {}".format(f, f_dir + "/" + tmp_f_name + f_ext))


def remove_duplicates(main_dir):
    """ Remove any duplicate images in each sub-dir"""

    duplicates = []
    hash_keys = dict()
    for index, filename in enumerate(os.listdir("E:/Mitch/Dropbox/Camera Uploads")):
        f_path = os.path.join("E:/Mitch/Dropbox/Camera Uploads", filename)
        if os.path.isfile(f_path):
            with open(f_path, 'rb') as f:
                filehash = hashlib.md5(f.read()).hexdigest()
            if filehash not in hash_keys:
                hash_keys[filehash] = f_path
            else:
                duplicates.append((f_path, hash_keys[filehash]))

    for f_dir, _, _ in os.walk(main_dir):
        print(f_dir)

        # Get all duplicates inside a directory
        # duplicates = []
        # hash_keys = dict()
        for index, filename in enumerate(os.listdir(f_dir)):
            f_path = os.path.join(f_dir, filename)
            if os.path.isfile(f_path):
                with open(f_path, 'rb') as f:
                    filehash = hashlib.md5(f.read()).hexdigest()
                if filehash not in hash_keys:
                    hash_keys[filehash] = f_path
                else:
                    duplicates.append((f_path, hash_keys[filehash]))

        # # Delete duplicates based on sorted
        # for row in duplicates:
        #     for f_path in sorted(row)[1:]:
        #         print("\tRemoving {}".format(f_path))
        #         os.remove(f_path)

    # Delete any duplicates that are in Camera Uploads
    for row in duplicates:
        for f_path in row:
            if "Camera" in f_path and os.path.isfile(f_path):
                os.remove(f_path)
 

if __name__ == "__main__":
    main_dir = "E:/Mitch/Dropbox/MyPhotos"
    # photo_rename_date(main_dir)
    remove_duplicates(main_dir)

