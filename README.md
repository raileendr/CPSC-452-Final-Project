# CPSC 452

## Final Project - Secure Messaging
<br>
In this project we implement a system which enables a group of users to chat securely.
All users are registered with the chat server. When the user wants to chat with another registered user, he first connects to the chat server and enters his/her user name and password.


The server verifies the user name and password, and if correct, the user’s status is changed to
“online". Next, the user may enter the user ids of users with whom he wishes to chat (could be
more then one). At any given time the user should be able to check what other users are online
and invite them to the ongoing conversation.


Once the user specifies the users with whom he wishes to chat, the server generates a symmetric
key, and securely distributes it to all the specified users and the user who initiated the chat. To
achieve secure key distribution you must encrypt the symmetric key using the public keys of the
respective users (you may assume that server knows the public keys of all users). If one of the
specified users is not online, the requesting user is notified about this.


After the encrypted symmetric key has been distributed to all users, the users decrypt the symmetric key using their private keys, and the chat session may begin. All messages exchanged during the chat must be encrypted using the symmetric key provided by the server and must be
delivered to all users participating in the chat. Any user may choose to leave the conversation.


If the user disconnects from the chat server, his status should be changed to “offline“. All users
who are connected to the server, must have a way to check whether a given user is online.


Our implementation must provides both confidentiality and digital signature. For digital signature, we provide the user with a choice of using RSA or Digital Signature Algorithm
(DSA; https://bit.ly/2TvvGSt). Both digital signature schemes are supported.


## Team Members
1. Raileen Del Rosario - raileendr@csu.fullerton.edu
2. Michael Lau - m.lau@csu.fullerton.edu
3. Garinn Morton - gmorton2@csu.fullerton.edu
4. Nafis Chowdhury - nafis195@csu.fullerton.edu
5. Ryan Romero - rromero26@csu.fullerton.edu
6. Jin Park - jinhpark9@csu.fullerton.edu
<br>

## Programming Language
C++
<br>

## Execution Process
TBA


## Special Notes
TBA
