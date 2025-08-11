import json
import re
# attribute
file_name = "list_contact.json"


# get data
def get_data(file_name):
    while True:
        try:
            with open(file_name, 'r') as files:
                data = json.load(files)
        except:
            set_contact()
        else:
            break
    return data


# check whether the data is really new
def valid_input(data, item):
    pattern = {
        'name': r"[_a-zA-Z]",
        'phone': r"^[+|0-9][ 0-9]*[0-9]$",
        'email': r"[a-zA-Z]\w+[@]\w+[.]\w"
    }
    input_criteria = {
        'name': "=> Name must begin with a letter.--",
        'phone': "=> Numbers must contain numbers and begin with a number or the character '+'.",
        'email': "=> E-mail does not match."
    }
    while True:
        value = input("input " + item + ": ")
        list_value = [x[item] for x in data if x[item] == value]
        if re.match(pattern[item], value):
            if value in list_value:
                print(item, "has been used.")
                continue
            else:
                break
        else:
            print(input_criteria[item])
            continue
    return value


# create contact
def create_contact(data):
    detail_inform = {}
    detail_inform['name'] = "Anonim"
    detail_inform['phone'] = "-"
    detail_inform['email'] = "-"
    name = valid_input(data, 'name')
    phone = valid_input(data, 'phone')
    email = valid_input(data, 'email')
    # check valid
    if name:
        detail_inform['name'] = name
    if phone:
        detail_inform['phone'] = phone
    if email:
        detail_inform['email'] = email
    return detail_inform


# set contact
def set_contact(list_contact=[]):
    list_contact = list_contact
    with open(file_name, 'w') as files:
        json.dump(list_contact, files)


# check the desired contact
def check_contact(id, data):
    print("is this contact what you mean?")
    print("name: ", data[id]['name'])
    print("Phone : ", data[id]['phone'])
    check = input("Press (y/n): ")
    return check


# search id contact
def search_id_contact(keyword, data):
    for key, value in enumerate(data):
        for contact in value.values():
            if keyword in contact:
                id_contact = key
                check = check_contact(id_contact, data)
                if check.lower() == 'y':
                    return id_contact
                else:
                    break


# search detail contact
def search_contact(data):
    keyword = input("input a keyword: ")
    key = search_id_contact(keyword, data)
    # ``search_id_contact`` returns ``None`` when the keyword isn't found.
    # The previous implementation used ``if str(key) or key == "None"`` which
    # always evaluated to ``True`` (since ``str(None)`` is the non-empty string
    # ``"None"``).  As a result the code attempted to index ``data[None]`` and
    # crashed with a ``TypeError`` whenever a contact wasn't found.  By checking
    # explicitly for ``None`` we only display details when a valid index is
    # returned.
    if key is not None:
        print("******************************")
        print("**  Contact has been found  **")
        print("******************************")
        for id_list, value in data[key].items():
            print("**", id_list, ":", value)
        print("******************************")
        return key
    else:
        print("Contact not found!!!!")


# update contact
def edit_contact(data):
    id_contact = search_contact(data)
    print("Input new data")
    print("-- ignore if you don't want to be changed. --")
    data_contact = create_contact(data)
    # check which parts have changed
    if data_contact['name'] == "Anonim":
        data_contact['name'] = data[id_contact]['name']
    if data_contact['phone'] == '-':
        data_contact['phone'] = data[id_contact]['phone']
    if data_contact['email'] == '-':
        data_contact['email'] = data[id_contact]['email']

    data[id_contact] = data_contact
    set_contact(data)
    print("Data has been changed successfully.")

# delete contact


def delete_contact(data):
    id_contact = search_contact(data)
    # ``search_contact`` returns ``None`` when the user doesn't confirm a
    # contact.  The previous check ``if str(id_contact)`` behaved the same as
    # ``if True`` even when ``id_contact`` was ``None``.  This meant the code
    # attempted to delete ``data[None]`` and failed.  Guard against this by
    # ensuring a valid index was returned before attempting the deletion.
    if id_contact is not None:
        check = input("Are you sure?  (y/n) ")
        if check.lower() == 'y':
            del data[id_contact]
            set_contact(data)
            print("Contact deleted successfully.")
