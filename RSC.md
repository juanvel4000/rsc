# RSC: Really Simple Communication
**Version**: 1.0
**Status**: Prototype
**Author**: juanvel400 <pda@juanvel400.xyz>
**Date**: 2025-04-12
**Transport**: HTTP
An Alternative to IRC, RSC is a standard for decentralized communication where each RSC node (Server) contains users and messages, it is designed to be small
RSC nodes are HTTP Servers that have implemented the 3 endpoints, those servers contain the uniqids, the usernames and the messages, its up to the user to trust them
Its recommended to use HTTPS for security reasons
# Users:
Users are assigned an uniqid (unique identificator) they use to send messages. Anyone with access to these uniqids can send messages under the user's name, each uniqid is aliased to an username, created by the user
# Endpoints:
- /user/create
 Description: Create a new user in the node
 POST Variables
 username: User's identificator, aliased to the uniqid
 Server response (on success)
 {"code": 200}
- /message/send
 Description: Send a message to the node
 POST Variables:
 uniqid: User's unique identificator
 contents: Message contents
 Server response (on success)
 {"code": 200}
- /message/get
 Description: Get all messages in the node
 Server response (on success)
 {"code": 200, [{"username": (message1 user's name), "contents": (message contents), "timestamp": (creation timestamp, format: 1970-01-01 00:00:00)} ...]}
