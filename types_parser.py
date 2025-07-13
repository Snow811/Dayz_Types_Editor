from lxml import etree

def load_types(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()

    items = []
    for elem in root.findall("type"):
        item = {
            "name": elem.attrib.get("name", ""),
            "nominal": get_text(elem, "nominal"),
            "lifetime": get_text(elem, "lifetime"),
            "restock": get_text(elem, "restock"),
            "min": get_text(elem, "min"),
            "quantmin": get_text(elem, "quantmin"),
            "quantmax": get_text(elem, "quantmax"),
            "cost": get_text(elem, "cost"),
            "flags": get_flags(elem),
            "category": get_attr(elem, "category", "name"),
            "tags": get_multi(elem, "tag"),
            "usage": get_multi(elem, "usage"),
            "value": get_multi(elem, "value")
        }
        items.append(item)

    return items, tree

def get_text(elem, tag):
    child = elem.find(tag)
    return child.text.strip() if child is not None and child.text else ""

def get_attr(elem, tag, attr):
    child = elem.find(tag)
    return child.attrib.get(attr, "") if child is not None else ""

def get_flags(elem):
    flags_elem = elem.find("flags")
    return {k: v for k, v in flags_elem.attrib.items()} if flags_elem is not None else {}

def get_multi(elem, tag):
    return [e.attrib["name"] for e in elem.findall(tag)]

def save_types(items, tree, output_path):
    root = etree.Element("types")

    for item in items:
        type_elem = etree.SubElement(root, "type", name=item["name"])

        def add(tag):
            val = str(item.get(tag, "")).strip()
            sub = etree.SubElement(type_elem, tag)
            sub.text = val

        # Ordered value tags
        for tag in ["nominal", "lifetime", "restock", "min", "quantmin", "quantmax", "cost"]:
            add(tag)

        etree.SubElement(type_elem, "flags", item.get("flags", {}))
        etree.SubElement(type_elem, "category", {"name": item.get("category", "")})

        for tag in item.get("tags", []):
            etree.SubElement(type_elem, "tag", {"name": tag})
        for usage in item.get("usage", []):
            etree.SubElement(type_elem, "usage", {"name": usage})
        for value in item.get("value", []):
            etree.SubElement(type_elem, "value", {"name": value})

    tree_str = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")

    with open(output_path, "wb") as f:
        f.write(tree_str)
