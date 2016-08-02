import ast, os
import yaml


exclude = ("tests", "static", "sampledata")


def is_private(name):
    if name.startswith("_", 0, 1) and name != "__init__":
        return True
    else:
        return False


def output_classes(file_path, filename):
    with open(file_path, "r") as f:
        source = f.read()
        p = ast.parse(source)
        classes = [node for node in ast.walk(p) if isinstance(node, ast.ClassDef) and not is_private(node.name)]
        class_defs = {"classes": {}}
        for x in classes:
            class_defs["classes"][x.name] = {}
            functions = []
            for y in x.body:
                if type(y) == ast.FunctionDef and not is_private(y.name):
                    functions.append(y.name)
            class_defs["classes"][x.name]["methods"] = functions
    return class_defs


def get_filenames(directory):
    files = []
    p = os.walk(directory, topdown=True, followlinks=False)
    for dirpath, dirnames, filenames in p:
        for d in exclude:
            if d in dirpath:
                break
        else:
            for x in filenames:
                if x.endswith(".py") and not x.startswith("_"):
                    files.append((dirpath + "/" + x, x))
    return files


def get_files_dict(filenames):
    files_dict = {}
    for x in filenames:
        files_dict[x[0]] = output_classes(x[0], x[1])
    return files_dict


def dump_yaml(source):
    with open("classes.yaml", "w") as stream:
        yaml.dump(source, stream, default_flow_style=False)

apple = get_files_dict(get_filenames("../bokeh"))
dump_yaml(apple)
