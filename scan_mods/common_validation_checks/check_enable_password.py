#!python

"""
Validator for the enable password 
"""

import getpass
import time


def check_enable_password(password, address):
    """
    Function will check to see if an enable password is given at runtime.  If not, it will ask the user if one is needed for the device
    If the user says one is needed it will attempt to get one from the user
    Args:
        password (None|str) : this will be None if no password is given or check to make sure a string otherwise.
        address (str) : string of the address getting password for
    return:
        str : password either validated or gotten from a user

    """
    while True:
        if not isinstance(address, str):
            raise ValueError(
                f"You gave me an address of {address} of type {type(address)}.  It needs to be a string."
            )
        if password is None or not isinstance(password, str):
            password = getpass.getpass(
                f"You have indicated that an enable password is required.  \n"
                f"Please enter your enable password for system at IP {address}: "
            )
        if password is not None and isinstance(password, str):
            if len(password) < 513:
                if len(password) > 0:
                    return password
                else:
                    print(
                        f"Password was less than 1 character.  Please re-enter the CORRECT enable password"
                    )
            else:
                print(
                    f"Password was greater than 512 characters."
                    f"  Please re-enter the CORRECT enable password because no password is really that long."
                )
            password = None


if __name__ == "__main__":
    start_time = time.time()
    password_list_to_test = [
        None,
        1,
        "a",
        "asdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkf",
        "asdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdfasdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdfasdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdf",
    ]
    address_for_test = "192.168.1.65"
    for password in password_list_to_test:
        print(f"The password is : {check_enable_password(password, address_for_test)}")

    duration = time.time() - start_time
    print(f"Duration to run was {duration}")
