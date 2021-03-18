#!python

"""
Function to check the username to make sure that it is valid
"""


import time


def check_username(name, address):
    """
    This will check to see if a username is given or if one needs to be asked for
    Args:
        name (None|str) : this will be None if no username is given or check to make sure a string otherwise.
        address (str) : string of the address getting username for
    return:
        str : username either validated or gotten from a user
    """
    while True:
        if not isinstance(address, str):
            raise ValueError(
                f"You gave me an address of {address} of type {type(address)}.  It needs to be a string."
            )
        if name is None or not isinstance(name, str):
            name = input(f"Please enter your username for system at IP {address}: ")
        if name is not None and isinstance(name, str):
            if len(name) < 255:
                if len(name) > 0:
                    return name
                else:
                    print(
                        f"Username was less than 1 character.  Please re-enter the CORRECT username"
                    )
            else:
                print(
                    f"Username was greater than 255 characters.  Why the heck did you do that?"
                )
            name = None


if __name__ == "__main__":
    start_time = time.time()
    usernames_to_test = [
        None,
        1,
        "a",
        "asdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkf",
        "asdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdf",
    ]
    address_for_test = "192.168.1.65"
    for name in usernames_to_test:
        print(f"The username is : {check_username(name, address_for_test)}")

    duration = time.time() - start_time
    print(f"Duration to run was {duration}")
