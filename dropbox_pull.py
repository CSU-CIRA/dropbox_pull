import dropbox
import os
import sys
import argparse

files_in_folder = []

def get_filenames(entries):
    for entry in entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            files_in_folder.append(entry.name)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="GeoCarb L2FP retrieval aggregation", prefix_chars="-")
    parser.add_argument("-d", "--dropbox_dir", help="URL to shared Dropbox directory", required=True)
    parser.add_argument("-o", "--output_dir", help="Path to local directory to put downloaded files", required=True)
    parser.add_argument("-t", "--token_file", help="Text file containing your Dropbox API Access Token", required=True)
    parser.add_argument("-v", "--verbose", help="Prints some basic information during code execution", action="store_true")
    args = parser.parse_args()

    verbose = args.verbose
    folder_url = args.dropbox_dir
    download_dir = args.output_dir
    token_file = args.token_file

    with open(token_file, "r") as tf:
        token = tf.read().strip()

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    shared_link_handle = dropbox.files.SharedLink(url=folder_url)
    dbx = dropbox.Dropbox(token)

    # Get initial list of files (first page)
    folder_entries_metadata = dbx.files_list_folder(path="", shared_link=shared_link_handle)
    get_filenames(folder_entries_metadata.entries)

    # Build list of all files in folder
    while folder_entries_metadata.has_more:
        folder_entries_metadata = dbx.files_list_folder_continue(folder_entries_metadata.cursor)
        get_filenames(folder_entries_metadata.entries)

    if verbose:
        print("Folder contains " + str(len(files_in_folder)) + " files")
        print("Starting download\n")

    # Download files
    for filename in files_in_folder:
        if verbose:
            print("Downloading " + filename)
        remote_path = "/" + filename
        local_path = os.path.join(download_dir, filename)
        dbx.sharing_get_shared_link_file_to_file(download_path=local_path, url=folder_url, path=remote_path)
        sys.exit()
