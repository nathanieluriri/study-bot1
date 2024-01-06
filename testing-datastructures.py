fruits = ["apple", "banana and sauce", "cherry"]

fruits_with_juice = [ {"apple":"apple juice"},{"banana and sauce":"banana juice"},{"cherry":"sosa cherry"}]




def get_key_and_value(dictionary, key):
    if key in dictionary:
        return key, dictionary[key]
    else:
        return None, None

# Example usage:
my_dict = {"a": 1, "b": 2, "c": 3}
search_key = "b"
key, value = get_key_and_value(my_dict, search_key)

if key is None:
    print(f"The key '{search_key}' was not found in the dictionary.")
else:
    print(f"Key: {key}, Value: {value}")




def check(look_for,lst):
    for checkme in lst:
        if look_for.strip() in checkme.strip():
            return f"{checkme}"
    return False


def look(look_for,dct):
    for checking in dct:
        if look_for in checking:
            return dct.index(checking),checking.get(look_for)

find = input(">:")

result = check(find,fruits)
print(result)
a,b =look(result,fruits_with_juice)
print(a,b)

def get_keys_and_values(dictionary):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    return keys, values

# Example usage:
my_dict = {"a": 1, "b": 2, "c": 3}
keys, values = get_keys_and_values(my_dict)
print("Keys:", str(keys))
print("Values:", str(values))



