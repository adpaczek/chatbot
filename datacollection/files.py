from pathlib import Path
import zipfile
import shutil
import os

srt_zip_path = Path('./datasets/srt/zip/good')
srt_unpacked_path = Path('./datasets/srt/unpacked')
srt_files_path = Path('./datasets/srt/files')
srt_format = ".srt"

sub_zip_path = Path('./datasets/sub/zip')
sub_unpacked_path = Path('./datasets/sub/unpacked')
sub_files_path = Path('./datasets/sub/files')
sub_format = ".txt"
sub_format2 = ".sub"


# Extraction of zip folders to destination folder
def extract_files(zip_path, destination_path):
    for path in zip_path.glob("*.zip"):
        print("Unpacking: " + str(path))
        with zipfile.ZipFile(path, 'r') as zf:
            final_path = destination_path / Path(path.stem)
            zf.extractall(path=final_path)


# Copying files only in specific format (.srt, .sub, .txt)
def copy_specific_files(source_folder, destination_folder, file_format):
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith(file_format):
                source_file_path = os.path.join(root, filename)
                destination_file_path = os.path.join(destination_folder, filename)
                shutil.copy(source_file_path, destination_file_path)


#extract_files(srt_zip_path, srt_unpacked_path)
#extract_files(sub_zip_path, sub_unpacked_path)

copy_specific_files(srt_unpacked_path, srt_files_path, srt_format)
#copy_specific_files(sub_unpacked_path, sub_files_path, sub_format)
#copy_specific_files(sub_unpacked_path, sub_files_path, sub_format2)
