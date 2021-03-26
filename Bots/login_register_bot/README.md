# Chatbot-Agent-handoff

## Rasa Chatbot with SQL DB

  - [ ] User Login/Register
    - [ ] Name, Email, OTP, Password
    - [ ] User will recieve OTP via mail and that he has to entered in chat.
  - [ ] Details will be stored local DB in
  - [ ] Integrate happy rasa bot
  - [ ] User will ask are u bot?
  - [ ] Agent handoff
    - [ ] A Link will be send to user mail along with unique randomly created room name, which will be used by user to enter the room. => this info will be posted to firebase.
    - [ ] POST request will be send with user info.

## Website 

- [ ] Server Side
  - [ ] Getting the POST request from chatbot. => firebase => UI
  - [ ] All the room name, user and their mail id along with time will be mentioned. => enlisted by FCFS.
  - [ ] CSR can choose to chat and start chatting. 
  - [ ] CSR can view his previous chats. (optional)
  - [ ] All the details will be stored in firebase and admins can view them.

- [ ] Client Side
  - [ ] Enter Your Room Name and Email. => validation with firebase
  - [ ] Chat page.
  - [ ] When Client leaves the chat session will get destroy. (or after 1hr)

## Addtional Functionalities

- [ ] When chatbot response contains keyword "password" change input type to password.