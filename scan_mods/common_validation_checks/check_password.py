#!python

"""
validation check for checking the password 
"""

import time
import getpass


def check_password(password, address):
    """
    This will check to see if a password is given or if one needs to be asked for
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
                f"Please enter your password for system at IP {address}: "
            )
        if password is not None and isinstance(password, str):
            if len(password) < 513:
                if len(password) > 0:
                    return password
                else:
                    print(
                        f"Password was less than 1 character.  Please re-enter the CORRECT password"
                    )
            else:
                print(
                    f"Password was greater than 512 characters."
                    f"  Please re-enter the CORRECT password because no password is really that long."
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
        print(f"The password is : {check_password(password, address_for_test)}")

    duration = time.time() - start_time
    print(f"Duration to run was {duration}")
