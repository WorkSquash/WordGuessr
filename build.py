import os
import shutil
import PyInstaller.__main__

# Build directory path
build_dir = os.path.expanduser("~/Documents/Games/WordGuessr")

# Create the directory if it doesn't exist
os.makedirs(build_dir, exist_ok=True)

# Copy assets to the build directory, replacing existing files
shutil.copytree('wordLists', os.path.join(build_dir, 'wordLists'), dirs_exist_ok=True)
shutil.copy2('categories.txt', build_dir)
shutil.copy2('version.txt', build_dir)
shutil.copy2('readme.txt', build_dir)

# Run PyInstaller to build the executable
PyInstaller.__main__.run([
    'wordguessr.spec',
    '--distpath',
    build_dir,
])
