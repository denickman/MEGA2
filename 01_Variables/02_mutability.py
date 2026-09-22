
filenames = ["1.raw data.txt", "2.second file.txt", "3.presentation.txt" ]

new_filenames = [f.replace('.', '-', 1) for f in filenames]


print(new_filenames)