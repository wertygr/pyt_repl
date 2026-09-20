from pyre_core import str_is_int

def alias_position_validate(alias_position: int, alias_settings: dict) -> bool:
    position =  alias_settings.get("position", None)
    if position is None:
        return True
    if isinstance(position, list) and alias_position in position:
        return True
    return False


def alias_paste(value: list[str], result: list[str], command_arg: list[str], alias_position: int) -> tuple[
    list[str], list[int]]:
    value_copy = value.copy()
    indices_to_remove = []

    for index, item in enumerate(value_copy):
        if item.startswith(">#") and str_is_int(item[2:]):
            goto_index = int(item[2:])
            target_index = alias_position + goto_index

            if 0 <= target_index < len(command_arg):
                value_copy[index] = command_arg[target_index]
                indices_to_remove.append(target_index)
                if goto_index < 0 and command_arg[target_index] in result:
                    result.remove(command_arg[target_index])
        elif item.startswith("!#") and str_is_int(item[2:]):
            target_index = int(item[2:])
            if 0 <= target_index < len(command_arg):
                value_copy[index] = command_arg[target_index]
                indices_to_remove.append(target_index)
                if target_index < alias_position and command_arg[target_index] in result:
                    result.remove(command_arg[target_index])

    result.extend(value_copy)
    return result, indices_to_remove


def alias_parser(alias_dict: dict, command_arg: list, mode: str) -> list[str]:
    result = []
    global_removals = set()

    index = 0
    while index < len(command_arg):
        if index in global_removals:
            index += 1
            continue

        item = command_arg[index]

        if not (item in alias_dict):
            result.append(item)
            index += 1
            continue

        item_dict = alias_dict.get(item, {})
        value = item_dict.get("value", "NONE_ALIAS")
        scope = item_dict.get("scope", "local")

        if (scope == mode) and (alias_position_validate(index, alias_dict[item])):
            result, removed_indices = alias_paste(value, result, command_arg, index)
            for r_idx in removed_indices:
                global_removals.add(r_idx)
            global_removals.add(index)
        else:
            result.append(item)

        index += 1
    for r_idx in sorted(global_removals, reverse=True):
        if r_idx < len(command_arg):
            command_arg.pop(r_idx)
    return result