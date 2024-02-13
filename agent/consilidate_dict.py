
def consolidate_duplicates(arr):
    append_text = "\n\n"

    consolidated = {}
    seen_keys = set()

    for dictionary in arr:
        for key, value in dictionary.items():
            if key in seen_keys:
                consolidated[key] = "\n```"+consolidated[key]+"```" + append_text + "```" + value + "\n```"
            else:
                consolidated[key] = value
                seen_keys.add(key)

    new_arr = [{key: value} for key, value in consolidated.items()]
    return new_arr