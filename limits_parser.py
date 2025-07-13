import xml.etree.ElementTree as ET

def parse_limits_definition(path):
    tree = ET.parse(path)
    root = tree.getroot()

    usage_flags = set()
    value_flags = set()
    categories = set()
    tags = set()

    for usage in root.findall(".//usage"):
        usage_flags.add(usage.attrib["name"])
    for value in root.findall(".//value"):
        value_flags.add(value.attrib["name"])
    for cat in root.findall(".//category"):
        categories.add(cat.attrib["name"])
    for tag in root.findall(".//tag"):
        tags.add(tag.attrib["name"])

    return {
        "usage": sorted(usage_flags),
        "value": sorted(value_flags),
        "categories": sorted(categories),
        "tags": sorted(tags)
    }

def parse_user_lists(path):
    tree = ET.parse(path)
    root = tree.getroot()

    usage_aliases = {}
    value_aliases = {}

    usage_section = root.find("usageflags")
    if usage_section is not None:
        for user in usage_section.findall("user"):
            name = user.attrib["name"]
            usage_aliases[name] = [u.attrib["name"] for u in user.findall("usage")]

    value_section = root.find("valueflags")
    if value_section is not None:
        for user in value_section.findall("user"):
            name = user.attrib["name"]
            value_aliases[name] = [v.attrib["name"] for v in user.findall("value")]

    return usage_aliases, value_aliases

def build_tag_config(def_path, user_path):
    base = parse_limits_definition(def_path)
    usage_aliases, value_aliases = parse_user_lists(user_path)

    usage_options = base["usage"] + list(usage_aliases.keys())
    value_options = base["value"] + list(value_aliases.keys())

    return {
        "usage": sorted(set(usage_options)),
        "value": sorted(set(value_options)),
        "usage_aliases": usage_aliases,
        "value_aliases": value_aliases,
        "categories": base["categories"],
        "tags": base["tags"]
    }
