# Python script to patch rsh.xml to create rsh_modified.xml using find-and-replace strategy

def patch_rsh_file(input_file, output_file):
    # Original and replacement text as specified in the diff
    replacements = {
        '<p><cite>eight</cite>. <info keyword="youngster"/><count/></p>': '<p><ignore>eight</ignore>. <info keyword="youngster"/><count/></p>',
        '<p><cite>dirt</cite>. <count/></p>': '<p><cite>dirt</cite> ...<cite>black</cite>. <count/></p>',
        '<frame xsi:type="character" number="186" character="洞" keyword="cave">': '<frame xsi:type="character" number="186" character="洞" keyword="cave‡">',
        '<p><cite>a drop of</cite> ... <cite>king</cite> ... <cite>jade</cite>. <count/></p>': '<p><cite>a drop of</cite> ... <cite>king</cite> ... <ignore>jade</ignore>. <count/></p>',
        '<p><cite>six</cite> ... <cite>animal legs</cite>. <count/></p>': '<p><ignore>six</ignore> ... <ignore>animal legs</ignore>. <count/></p>',
        '<frame xsi:type="character" number="788" character="箱" keyword="box" pos="n.">': '<frame xsi:type="character" number="788" character="箱" keyword="box‡" pos="n.">'
    }

    # Read the original file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Apply replacements
    for i, line in enumerate(lines):
        original_line = line.strip()
        if original_line in replacements:
            lines[i] = replacements[original_line] + '\n'

    # Verify all replacements were made
    for original, replacement in replacements.items():
        if original in ''.join(lines):
            raise ValueError(f"Replacement for line not found: {original}")

    # Write to the modified file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# File paths
input_file = 'data/rsh.xml'
output_file = 'data/rsh_modified.xml'

# Patch the file
patch_rsh_file(input_file, output_file)
