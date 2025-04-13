from framework import RSCClient
import sys
import os
import configparser
import json
def _main():
    args = sys.argv
    if len(args) < 2:
        print("!> Missing arguments, try \"help\"")
        sys.exit(1)

    config = configparser.ConfigParser()
    rsccfg = os.path.join(os.path.expanduser('~'), '.RSCConfig')

    if not os.path.isfile(rsccfg):
        with open(rsccfg, 'w') as x:
            x.write('[RSC]\nUUID=False\nServer=False')

    config.read(rsccfg)
    
    if 'RSC' not in config:
        print("!> Missing [RSC] section in config file")
        sys.exit(1)

    server = config.get('RSC', 'Server')
    uuid = config.get('RSC', 'UUID')

    if server == "False":
        server = input("?> Enter your RSC Server: ")
        config.set('RSC', 'Server', server)
        with open(rsccfg, 'w') as configfile:
            config.write(configfile)

    rsc = RSCClient(server)

    match args[1]:
        case 'login':
            print("1 : Use an existing UUID")
            print("2 : Create a new user")
            select = input("?> How do you want to login?: ")

            if select == "1":
                uuid = input("?> Enter your UUID: ")
                config.set('RSC', 'UUID', uuid)
                with open(rsccfg, 'w') as configfile:
                    config.write(configfile)
            else:
                new_username = input("?> Enter your new username: ")
                uuid = rsc.create(new_username)
                config.set('RSC', 'UUID', uuid)
                with open(rsccfg, 'w') as configfile:
                    config.write(configfile)

        case 'chat':
            if uuid == "False":
                print(f"!> Please login using the argument \"login\"")
                sys.exit(1)
            print(f"Logged in with UUID: {uuid}")
            rsc.login(uuid)
            x = False
            while True:
                if x != True:
                    contents = rsc.get()
                
                    for i in contents['messages']:
                        print(f"{i['username']} - {i['timestamp']}")
                        print(i['contents'])
                else:
                    x = False
                res = input("you> ")
                if res == "/cli exit":
                    break
                if res == "/cli help":
                    print("RSC CLI")
                    print("Commands:")
                    print("- help - Show this message")
                    print("- exit - Exit the chat")
                    x = True
                    continue

                rsc.send(res)
        case 'help':
            print("RSC CLI")
            print(" login  -   -    Login with your UUID")
            print(" chat       -    Enter the server chatroom")
            print("Use /cli help in the chat to view the chat-commands")
        case _:
            print(f"!> Unknown argument \"{args[1]}\"")
            sys.exit(1)

if __name__ == "__main__":
    _main()
