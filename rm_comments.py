#! python==3.6.8
import os
import shutil


def main(path):
    """

    :param path: the root path need clean the comments and space line
    :return:
    """
    # print("dir:" + path)
    new_dir = path[:path.rfind("\\")] + path[path.rfind("\\"):] + "_new"
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    shutil.copytree(path, new_dir)
    for root, dirs, files in os.walk(new_dir):
        # print("***")
        # print(files)
        for name in files:
            # print(name)
            if name.endswith(r".py"):  # only handle the .py files
                trim_file(os.path.join(root, name))


def trim_file(path):
    """

    """
    content = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        flag = 1
        for line in lines:
            s = line.strip()

            if s == '"""' or s == "'''":
                flag *= -1
            elif s.startswith(r"'''") and s.endswith(r"'''"):
                pass
            elif s.startswith(r'"""') and s.endswith('"""'):
                pass
            elif s.startswith(r'"""') or s.endswith('"""') or s.startswith(r"'''") or s.endswith(
                    "'''"):  # lines in """    """
                flag *= -1
            elif flag == -1:
                pass

            elif s.startswith("#"):  # lines start with #
                pass
            elif line.startswith("\n"):  # null lines
                pass
            elif hash_line(line)['res']:  # line with # in the middle
                content.append(hash_line(line)['new_line'])
            else:
                content.append(line)
    with open(path, 'w+', encoding='utf-8') as f:
        f.writelines(content)
        print("{} update complete".format(path))

    return


def hash_line(line):
    res = False
    new_line = ""
    if '#' in line:
        comment = line[line.find("#"):]
        if "\'" not in comment and '\"' not in comment:  # check the "#" belong to strings or not
            res = True
            new_line = line[:line.find("#")] + "\n"

    return {"res": res, "new_line": new_line}


