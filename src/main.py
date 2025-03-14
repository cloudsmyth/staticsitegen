import os
import shutil


def main():
    source = "static"
    dest = "public"
    copy_dirs(source, dest)


def copy_dirs(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist")
        return

    if os.path.exists(dest_dir):
        print("Cleaning out destination dir...")
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    recursive_copy(source_dir, dest_dir)
    print("Copying complete!")


def recursive_copy(source_dir, dest_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(source_path):
            if not os.path.exists(dest_path):
                print(f"Directory made: {dest_path}")
                os.mkdir(dest_path)
            recursive_copy(source_path, dest_path)
        else:
            shutil.copy(source_path, dest_path)


main()
