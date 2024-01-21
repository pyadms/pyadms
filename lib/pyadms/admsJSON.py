import os
import sys
import subprocess
def run():
    binary=[os.path.join(os.path.dirname(__file__), 'admsJSON')]
    binary.extend(sys.argv[1:])
    print(binary)
    subprocess.run(binary)
