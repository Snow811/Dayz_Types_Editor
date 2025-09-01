from lxml import etree as ET

def load_types(path):
    tree = ET.parse(path)
    root = tree.getroot()
    items = []

    for type_elem in root.findall("type"):
        item = {
            "name": type_elem.get("name", ""),
            "nominal": get_text(type_elem, "nominal"),
            "lifetime": get_text(type_elem, "lifetime"),
            "restock": get_text(type_elem, "restock"),
            "min": get_text(type_elem, "min"),
            "quantmin": get_text(type_elem, "quantmin"),
            "quantmax": get_text(type_elem, "quantmax"),
            "cost": get_text(type_elem, "cost"),
            "flags": {},
            "category": "",
            "usage": [],
            "value": [],
            "tags": []
        }

        flags_elem = type_elem.find("flags")
        if flags_elem is not None:
            for attr in ["count_in_cargo", "count_in_hoarder", "count_in_map", "count_in_player", "crafted", "deloot"]:
                item["flags"][attr] = flags_elem.get(attr, "0")

        cat_elem = type_elem.find("category")
        if cat_elem is not None:
            item["category"] = cat_elem.get("name", "")

        for tag in type_elem.findall("usage"):
            item["usage"].append(tag.get("name", ""))
        for tag in type_elem.findall("value"):
            item["value"].append(tag.get("name") or tag.get("user", ""))
        for tag in type_elem.findall("tag"):
            item["tags"].append(tag.get("name", ""))
        
        # Handle user-defined tags
        for user_tag in type_elem.findall("user"):
            if user_tag.get("usage"):
                item["usage"].append(user_tag.get("usage"))
            if user_tag.get("value"):
                item["value"].append(user_tag.get("value"))

        items.append(item)

    return items, tree

def get_text(elem, tag):
    child = elem.find(tag)
    return child.text if child is not None and child.text is not None else ""

def save_types(items, tree, path, map_mode="vanilla", tag_config=None):
    root = tree.getroot()
    root.clear()

    for item in items:
        type_elem = ET.SubElement(root, "type", name=item["name"])

        def add(tag):
            if item[tag]:
                ET.SubElement(type_elem, tag).text = item[tag]

        add("nominal")
        add("lifetime")
        add("restock")
        add("min")
        add("quantmin")
        add("quantmax")
        add("cost")

        flags_elem = ET.SubElement(type_elem, "flags")
        for attr in ["count_in_cargo", "count_in_hoarder", "count_in_map", "count_in_player", "crafted", "deloot"]:
            flags_elem.set(attr, item["flags"].get(attr, "0"))

        if item["category"]:
            ET.SubElement(type_elem, "category").set("name", item["category"])

        if map_mode == "vanilla":
            for tag in item["usage"]:
                # Check if this is a user-defined alias
                if tag_config and tag in tag_config.get("usage_aliases", {}):
                    ET.SubElement(type_elem, "user").set("usage", tag)
                else:
                    ET.SubElement(type_elem, "usage").set("name", tag)
            for tag in item["value"]:
                # Check if this is a user-defined alias
                if tag_config and tag in tag_config.get("value_aliases", {}):
                    ET.SubElement(type_elem, "user").set("value", tag)
                else:
                    ET.SubElement(type_elem, "value").set("name", tag)
        elif map_mode == "namalsk":
            for tag in item["value"]:
                ET.SubElement(type_elem, "value").set("user", tag)
            for tag in item["tags"]:
                ET.SubElement(type_elem, "tag").set("name", tag)

    tree.write(path, pretty_print=True, xml_declaration=True, encoding="utf-8")
