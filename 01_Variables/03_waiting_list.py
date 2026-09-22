import os

waiting_list = ['den', 'alex', 'nestor']
waiting_list.sort()



waiting_list2 = ['den.', 'alex.', 'nestor.']


updated_waiting_list = [name.replace(".", "-" + "txt") for name in waiting_list2]
print(updated_waiting_list)



for index, item in enumerate(waiting_list):
    row = f"{index+1}.{item.capitalize()}"
    print(row)




contents = ["All carrots are to be sliced "
            "longitudinally.",
            "The carrots were reportedly sliced.",
            "The slicing process was well presented."]

filenames = ["doc.txt", "report.txt", "presentation.txt"]


#
# for content, filename in zip(contents, filenames):
#     print(f"File: {filename}: - Content: {content}")





already_exist = False

for content, filename in zip(contents, filenames):
    path = f"files/{filename}"
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(content)
    else:
        if not already_exist:
            print("--already exist---")
            already_exist = True
        print(f"File {filename}: - Content: {content}")



a = "I am a string " \
    "on my " \
    "own"