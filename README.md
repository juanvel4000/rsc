
# RSC

**RSC** is a standard for decentralized communication


## Installation

You can write your own RSC node, its recommended to use the sample one `server.py` for newbies

```bash
  pip install flask
```
If you want, create a virtualenv

Steps for Linux:
```
  python -m venv venv
  source venv/bin/activate
```
Steps for Windows
```
  python -m venv venv
  venv/bin/Activate
```
Then you can install Flask with
```
  pip install flask
```


## Usage

### Server
You have to host an RSC node, `server.py` is a sample implementation of a RSC node written in python, Its recommended for newbies, you need to install Flask

Run `server.py`, by default it runs at [127.0.0.1:1819](http://127.0.0.1:1819)

## Client
Once you have an RSC node, you need a client, `cli.py`is a simple RSC client that uses the `RSCClient` class from `framework.py` its recommended to use the `RSCClient` class when building an RSC client

1. **Login with your UUID or create an user**, The first time you open `cli.py`, it asks for the server, enter the URL to your RSC node, or enter `http://127.0.0.1:1819` if you are selfhosting
```
cli.py login
```

2. **Enter the server**. Use `cli.py` to enter the server
```
cli.py chat
```
Run `/cli help` to view a list of commands you can run in the chat
