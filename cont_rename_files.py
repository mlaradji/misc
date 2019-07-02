"""
A sequential batch file renamer. This was designed to be used with the '2029 Radio- Pipboy Custom Radio' mod (https://www.nexusmods.com/fallout4/mods/28666) for Fallout 4.
"""

from pathlib import Path
import argparse
import hashlib
import shutil
import time



parser = argparse.ArgumentParser(
    description='A sequential batch file renamer.')
parser.add_argument(
    '--base', default=".", type=str,
    help='The path to the directory containing the files to be renamed.')
parser.add_argument(
    '--min', default=1, type=int,
    help='Renamed files will start from this integer.')
parser.add_argument(
    '--max', default=100, type=int,
    help='Renamed files will end at this integer. Exceeding this limit will raise a TooManyFiles error.')
parser.add_argument(
    '--dedup', const=True, default=False, action='store_const',
    help='Remove duplicate files.')
parser.add_argument(
    '--fill', const=True, default=False, action='store_const',
    help='Copy the last unique file until the max number of files is achieved.')
parser.add_argument(
    '--suffix', default=".wav", type=str,
    help="Only files with this suffix will be considered."
)
parser.add_argument(
    '--output-format', default="{i}{args.suffix}", type=str,
    help='All renamed files will have this format. Possible variables: i (index), filehash (sha256).'
)

class TooManyFiles(Exception):
    pass

if __name__ == "__main__":

    args=parser.parse_args()

    base: Path = Path(args.base)
    
    filehashes = set()
    seen_files = set(["cont_rename_files.py"])
    i: int = 0

    while True:
        for file in filter(lambda f: f.name not in seen_files, base.iterdir()):
            print(file.name)
            hasher = hashlib.sha256()
            hasher.update(file.read_bytes())
            filehash = hasher.digest()

            if args.dedup and filehash in filehashes:
                file.unlink()
                continue
                    

            # Check if the file already has a valid name.
            try:
                assert args.min <= int(file.stem)
            except (AssertionError, ValueError):
                pass
            else:
                filehashes.add(filehash)
                seen_files.add(file.name)
                continue
                    
            # Rename the file to the next available integer.
            while True:

                i += 1
                new_name = f"{i}{file.suffix}"

                try:
                    file.rename(new_name)
                except FileExistsError:
                    continue
                else:
                    filehashes.add(filehash)
                    seen_files.add(new_name)
                    break

        print(seen_files)
        time.sleep(1)

    # if args.fill:
    # 	while i < args.max:
    # 		i += 1
    # 		filecopy = base / args.output_format.format()
    # 		shutil.copy(str(file), str(filecopy))
