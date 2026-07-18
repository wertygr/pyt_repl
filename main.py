
# ver 0.0.1
simple_shell_command_API = {
    "item": None
}
logo_2 ="""
▒▒▒▒▒▒▒▒▒██████████████████
▒▒▒▒▒▒▒▒▒█▒██▒██▒██▒██▒██▒█
▒▒▒▒▒▒▒▒▒██████████████████
▒▒▒▒▒▒▒▒▒███▒▒▒██████▒▒▒███
▒▒▒▒▒▒▒▒▒█▒█▒▒▒█▒██▒█▒▒▒█▒█
▒▒▒▒▒▒▒▒▒███▒▒▒██████▒▒▒███
▒▒▒▒▒▒▒▒▒██████████████████
▒▒▒▒▒▒▒▒▒█▒██▒██▒██▒██▒██▒█
▒▒▒▒▒▒▒▒▒██████████████████
█████████▒▒▒▒▒▒▒▒▒█████████
█▒██▒██▒█▒██▒▒▒██▒█▒██▒██▒█
█████████▒█▒▒█▒▒█▒█████████
███▒▒▒███▒▒▒█▓█▒▒▒███▒▒▒███
█▒█▒▒▒█▒█▒▒█▓█▓█▒▒█▒█▒▒▒█▒█
███▒▒▒███▒▒▒█▓█▒▒▒███▒▒▒███
█████████▒█▒▒█▒▒█▒█████████
█▒██▒██▒█▒██▒▒▒██▒█▒██▒██▒█
█████████▒▒▒▒▒▒▒▒▒█████████
██████████████████▒▒▒▒▒▒▒▒▒
█▒██▒██▒██▒██▒██▒█▒▒▒▒▒▒▒▒▒
██████████████████▒▒▒▒▒▒▒▒▒
███▒▒▒██████▒▒▒███▒▒▒▒▒▒▒▒▒
█▒█▒▒▒█▒██▒█▒▒▒█▒█▒▒▒▒▒▒▒▒▒
███▒▒▒██████▒▒▒███▒▒▒▒▒▒▒▒▒
██████████████████▒▒▒▒▒▒▒▒▒
█▒██▒██▒██▒██▒██▒█▒▒▒▒▒▒▒▒▒
██████████████████▒▒▒▒▒▒▒▒▒

"""

logo = """
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@
               @@[]@@@[]@@[]@@[]@@@[]@@[]@@
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@
               @@[]@@   @@[]@@[]@@   @@[]@@
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@
               @@[]@@@[]@@[]@@[]@@@[]@@[]@@
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@  **     **# @@@@@@@@@@@@@@@
@@[]@@@[]@@[]@@ *********** @@[]@@@[]@@[]@@
@@@@@@@@@@@@@@@ ** **=** *# @@@@@@@@@@@@@@@
@@[]@@   @@[]@@  **+=*=+**  @@[]@@   @@[]@@
@@@@@@@@@@@@@@@ ** **=** ** @@@@@@@@@@@@@@@
@@[]@@@[]@@[]@@ *********** @@[]@@@[]@@[]@@
@@@@@@@@@@@@@@@ ***#   #*** @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@            
@@[]@@@[]@@[]@@[]@@@[]@@[]@@            
@@@@@@@@@@@@@@@@@@@@@@@@@@@@            
@@[]@@   @@[]@@[]@@   @@[]@@            
@@@@@@@@@@@@@@@@@@@@@@@@@@@@            
@@[]@@@[]@@[]@@[]@@@[]@@[]@@            
@@@@@@@@@@@@@@@@@@@@@@@@@@@@            

"""
import sys
import json
import os
import shutil
import uuid
import datetime


script_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(script_dir, "../project", "settings.json")

def settings_load():
    global id_pack, version, description, name, type_addon
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
            id_pack = settings["id_pack"]
            version = settings["version"]
            description = settings["description"]
            name = settings["name"]
            type_addon = settings["type"]
    except :
        shutil.copyfile(f"{script_dir}/resource/project_settings.json", f"{script_dir}/project/settings.json")


settings_load()

try:
    sub_flag = True
    type_id = sys.argv[1]
    argument = type_id.split()
except:
    sub_flag = False
    type_id = input("?>")
    argument = type_id.split()


def create_project(id_pack, name, version, type):

    settings_example_path = os.path.join(script_dir, "../resource", "project_settings.json")
    settings_path = os.path.join(script_dir, "../project", "settings.json")

    if not os.path.exists("../project/bh"):
        os.mkdir("../project/bh")
    if not os.path.exists("../project/bh/items"):
        os.mkdir("../project/bh/items")
    if not os.path.exists("../project/bh/functions"):
        os.mkdir("../project/bh/functions")
    if not os.path.exists("../project/rp"):
        os.mkdir("../project/rp")
    if not os.path.exists("../project/rp/texts"):
        os.mkdir("../project/rp/texts")
    if not os.path.exists("../project/rp/textures"):
        os.mkdir("../project/rp/textures")
    if not os.path.exists("../project/rp/textures/items"):
        os.mkdir("../project/rp/textures/items")
    if not os.path.exists(f"{script_dir}/build"):
        os.mkdir(f"{script_dir}/build")

    with open(settings_example_path, "r", encoding="utf-8") as f:
        example_settings = json.load(f)

    example_settings["id_pack"] = id_pack
    example_settings["version"] = version
    example_settings["name"] = name
    example_settings["type"] = type

    try:
        with open(settings_path, "x", encoding="utf-8") as f:
            json.dump(example_settings, f, indent=4, ensure_ascii=False)
    except:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(example_settings, f, indent=4, ensure_ascii=False)

    def local(lang):
        rp_dir = os.path.join(script_dir, "../project", "rp", "texts")
        output_lang_path = os.path.join(rp_dir, f"{lang}")
        try:
            with open(output_lang_path, "x", encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print(e)

    local("en_US.lang")
    local("ru_RU.lang")

    rp_dir = os.path.join(script_dir, "../project", "rp", "textures")
    rs_dir = os.path.join(script_dir, "../resource")
    example_item_textures_path = os.path.join(rs_dir, "item_texture_example.json")
    output_item_textures_path = os.path.join(rp_dir, "item_texture.json")

    if not os.path.exists(output_item_textures_path):
        with open(example_item_textures_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(output_item_textures_path, "x", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    settings_load()


def item_json(id_name, stack, lang_name, lang_name_ru, glint):


    template_path = os.path.join(script_dir, "../resource", "item_example.json")

    if stack > 64:
        stack = 64
    elif stack == 0:
        stack = 1
    elif stack < 0:
        stack = 1

    if glint == "t":
        glint = True
    elif glint == "f":
        glint = False

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(e)

    data["minecraft:item"]["description"]["identifier"] = f"{id_pack}:{id_name}"
    data["format_version"] = version
    data["minecraft:item"]["components"]["minecraft:icon"]= f"{id_pack}:{id_name}"
    data["minecraft:item"]["components"]["minecraft:glint"] = glint

    if "components" in data:
        data["minecraft:item"]["components"]["minecraft:max_stack_size"] = stack
    elif "components" in data.get("minecraft:item", {}):
        data["minecraft:item"]["components"]["minecraft:max_stack_size"] = stack



    bh_dir = os.path.join(script_dir, "../project", "bh", "items")
    rp_dir = os.path.join(script_dir, "../project", "rp", "texts")
    os.makedirs(bh_dir, exist_ok=True)

    output_path = os.path.join(bh_dir, f"{id_name}.json")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)
    def local(lang,lang_name):
        lang_name = lang_name.replace("_", " ")
        output_lang_path = os.path.join(rp_dir, f"{lang}")
        try:
            with open(output_lang_path, "a", encoding="utf-8") as f:
                f.write(f"item.{id_pack}:{id_name}.name={lang_name}\nitem.{id_pack}:{id_name}={lang_name}\n\n")

        except Exception as e:
            print(e)
    local("en_US.lang",lang_name)
    local("ru_RU.lang",lang_name_ru)

    def texture():
        rp_dir = os.path.join(script_dir, "../project", "rp")
        texture_path_rp = f"textures/items/{id_pack}_{id_name}"
        output_textures_path = os.path.join(rp_dir,"textures", "item_texture.json")
        with open(output_textures_path, "r", encoding="utf-8") as f:
            textures_data = json.load(f)
        textures_data["texture_data"][f"{id_pack}:{id_name}"] = {
            "textures": f"{texture_path_rp}"
        }
        with open(output_textures_path, "w", encoding="utf-8") as f:
            json.dump(textures_data, f, indent=4, ensure_ascii=False)

        texture_example = f"{script_dir}/resource/example_textures.png"
        texture_path = f"{rp_dir}/textures/items/{id_pack}_{id_name}.png"

        shutil.copy(texture_example, texture_path)
    texture()


def function(fn_name, command_filtration):
    bh_dir = os.path.join(script_dir, "../project", "bh", "functions")
    functions_path = os.path.join(bh_dir, f"{fn_name}.mcfunction")
    try:
        with open(functions_path, "x", encoding="utf-8") as f:
            f.write(f"{command_filtration}")
    except:
        with open(functions_path, "w", encoding="utf-8") as f:
            f.write(f"{command_filtration}")

def build():
    with open(os.path.join(script_dir, "../resource", "manifest", "bh_manifest.json"), "r", encoding="utf-8") as f:
        bh_manifest = json.load(f)
    with open(os.path.join(script_dir, "../resource", "manifest", "rp_manifest.json"), "r", encoding="utf-8") as f:
        rp_manifest = json.load(f)

    uuid_1 = str(uuid.uuid4())
    uuid_2 = str(uuid.uuid4())
    uuid_3 = str(uuid.uuid4())
    uuid_4 = str(uuid.uuid4())
    uuid_5 = str(uuid.uuid4())

    bh_manifest["description"] = description
    bh_manifest["header"]["name"] = name

    bh_manifest["header"]["uuid"] = uuid_1
    bh_manifest["modules"][0]["uuid"] = uuid_2
    bh_manifest["modules"][1]["uuid"] = uuid_3
    bh_manifest["dependencies"][0]["uuid"] = uuid_4

    rp_manifest["header"]["uuid"] = uuid_4
    rp_manifest["modules"][0]["uuid"] = uuid_5
    rp_manifest["dependencies"][0]["uuid"] = uuid_1

    rp_manifest["header"]["name"] = name
    rp_manifest["header"]["description"] = description
    rp_manifest["modules"][0]["description"] = description

    if not os.path.exists(os.path.join(script_dir, "../project", "rp", "manifest.json")):
        with open(os.path.join(script_dir, "../project", "rp", "manifest.json"), "x", encoding="utf-8") as f:
            f.write("")
    try:
        with open(os.path.join(script_dir, "../project", "rp", "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(rp_manifest, f, indent=4, ensure_ascii=False)
    except:
        with open(os.path.join(script_dir, "../project", "rp", "manifest.json"), "x", encoding="utf-8") as f:
            json.dump(rp_manifest, f, indent=4, ensure_ascii=False)

    if not os.path.exists(os.path.join(script_dir, "../project", "bh", "manifest.json")):
        with open(os.path.join(script_dir, "../project", "bh", "manifest.json"), "x", encoding="utf-8") as f:
            f.write("")
    try:
        with open(os.path.join(script_dir, "../project", "bh", "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(bh_manifest, f, indent=4, ensure_ascii=False)
    except:
        with open(os.path.join(script_dir, "../project", "bh", "manifest.json"), "x", encoding="utf-8") as f:
            json.dump(bh_manifest, f, indent=4, ensure_ascii=False)


    shutil.copy(f"{script_dir}/resource/example_textures.png", f"{script_dir}/project/rp/pack_icon.png")
    shutil.copy(f"{script_dir}/resource/example_textures.png", f"{script_dir}/project/bh/pack_icon.png")

    now = datetime.datetime.now()
    time = str(now.strftime("%H_%M_%S"))

    zip_build = os.path.join(script_dir, "../project")
    build_name = f"{name}"+"_"+time

    build_path = os.path.join(script_dir, "../build", f"{build_name}")

    shutil.make_archive(build_path, "zip", zip_build)

    os.rename(os.path.join(script_dir, "../build", f"{build_name}.zip"), f"{script_dir}/build/{build_name}.{type_addon}")


def clr_build():
    shutil.rmtree(os.path.join(script_dir, "../build"))
    os.mkdir(os.path.join(script_dir, "../build"))


def local(lang, string_add):
    if lang == "en":
        with open(f"{script_dir}/project/rp/texts/en_US.lang", "a", encoding="utf-8") as f:
            f.write(f"\n{string_add}\n")
    else:
        with open(f"{script_dir}/project/rp/texts/ru_RU.lang", "a", encoding="utf-8") as f:
            f.write(f"\n{string_add}\n")




def delete_(type_delete, id_delete):
    if type_delete == "item":
        try:
            os.remove(f"{script_dir}/project/bh/items/{id_delete}.json")
        except:
            pass
        try:
            os.remove(f"{script_dir}/project/rp/textures/items/{id_pack}_{id_delete}.png")
        except:
            pass
        with open(f"{script_dir}/project/rp/textures/item_texture.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            del data["texture_data"][f"{id_pack}:{id_delete}"]
        except:
            pass
        with open(f"{script_dir}/project/rp/textures/item_texture.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        def lang_delete(lang_delite):
            with open(f"{script_dir}/project/rp/texts/ru_RU.lang", "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(f"{script_dir}/project/rp/texts/ru_RU.lang", 'w', encoding='utf-8') as f:
                for line in lines:
                    if not line.strip().startswith(lang_delite):
                        f.write(line)

            with open(f"{script_dir}/project/rp/texts/en_US.lang", "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(f"{script_dir}/project/rp/texts/en_US.lang", 'w', encoding='utf-8') as f:
                for line in lines:
                    if not line.strip().startswith(lang_delite):
                        f.write(line)

        lang_delete(f"item.{id_pack}:{id_delete}")
    elif type_delete == "function":
        os.remove(f"{script_dir}/project/bh/functions/{id_delete}.mcfunction")

    if type_delete == "local":
        with open(f"{script_dir}/project/rp/texts/ru_RU.lang", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(f"{script_dir}/project/rp/texts/ru_RU.lang", 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.strip().startswith(id_delete):
                    f.write(line)

        with open(f"{script_dir}/project/rp/texts/en_US.lang", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(f"{script_dir}/project/rp/texts/en_US.lang", 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.strip().startswith(id_delete):
                    f.write(line)


type_id = argument[0]
if type_id == "item":

    try:
        name = argument[1]
        max_stack = int(argument[2])
        lang_name = argument[3]
        lang_name_ru = argument[4]
        glint = argument[5]
        item_json(name, max_stack, lang_name, lang_name_ru, glint)
    except IndexError:
        sys.exit(1)

elif type_id == "function":
    try:
        name = argument[1]
        command_filtration = [0,1]
        command = " ".join([word for i, word in enumerate(argument) if i not in command_filtration])
        function(name, command)
    except:
        sys.exit(1)

elif type_id == "create":
    try:
        id_pack = argument[1]
        name = argument[2]
        version = argument[3]
        type_addon = argument[4]
        create_project(id_pack, name, version, type_addon)
    except:
        sys.exit(1)

elif type_id == "build":
    try:
        build()
    except Exception as e:
        print(e)

elif type_id == "clr_build":
    clr_build()

elif type_id == "local":
    lang = argument[1]
    lang_filtration = [0, 1]
    string_add = " ".join([word for i, word in enumerate(argument) if i not in lang_filtration])
    local(lang, string_add)

elif type_id == "delete":
    type_delete = argument[1]
    id_delete = argument[:2]
    delete_(type_delete, id_delete)

elif type_id == "logo":
    print(logo)

else:
    print("no command")

if sub_flag == False:
    input()
