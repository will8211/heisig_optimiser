import os
import subprocess

# Directory containing the .diag files
diagrams_dir = "diagrams"

# Change to the diagrams directory
os.chdir(diagrams_dir)

# Fetch all filenames in the directory
filenames = [f for f in os.listdir() if f.endswith(".diag")]

# Run `blockdiag [filename]` on all files
for filename in filenames:
    try:
        result = subprocess.run(
            ["blockdiag", filename],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"Successfully processed {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {filename}: {e.stderr.decode('utf-8')}")
