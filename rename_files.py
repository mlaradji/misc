"""
A sequential batch file renamer. This was designed to be used with the '2029 Radio- Pipboy Custom Radio' mod (https://www.nexusmods.com/fallout4/mods/28666) for Fallout 4.
"""

from pathlib import Path
import argparse
import hashlib
import shutil



parser = argparse.ArgumentParser(
	description='Rename wav files to be used in.')
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
	
	filehashes: set = set()
	i: int = 0

	for file in base.iterdir():
		if file.suffix == args.suffix:
	
			if args.dedup:
				# Check if the file has been seen before.
				hasher = hashlib.sha256()
				hasher.update(file.read_bytes())
				filehash = hasher.digest()

				if filehash in filehashes:
					file.unlink()
				else:
					filehashes.add(filehash)

			# Check if the file already has a valid name.
			try:
				assert args.min <= int(file.stem) <= args.max
			except (AssertionError, ValueError):
				pass
			else:
				continue
					
			# Rename the file to the next available integer.
			while True:

				i += 1
				
				if i > args.max: raise TooManyFiles(i)

				try:
					file.rename(args.output_format.format())
				except FileExistsError:
					continue
				else:
					break

	if args.fill:
		while i < args.max:
			i += 1
			filecopy = base / args.output_format.format()
			shutil.copy(str(file), str(filecopy))
