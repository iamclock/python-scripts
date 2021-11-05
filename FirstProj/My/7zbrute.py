import subprocess
import sys

def main():
	archive = sys.argv[1]
	dictionary = sys.argv[2]
	with open(dictionary, "r") as dic:
		for line in dic:
				word = line.rstrip('\n')
				stdout = subprocess.call(
					"C:\Program Files\7-Zip\7z.exe t -p'{0}' {1}".format(word, archive), 
					stderr=subprocess.DEVNULL, 
					stdout=subprocess.DEVNULL, 
					shell=True
				)
				if stdout == 0:
					print("Password found: " + word)
					return
	print("Password not found.")

if __name__ == "__main__":
	if len(sys.argv) == 3:
		main()
	else:
		print("missing args")