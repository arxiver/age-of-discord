from db import create_user, create_server, join_server, send_message_to, get_messages_of

if __name__ == '__main__':
  # Create user 
  user1 = create_user("Mohamed", "mohamed")
  
  # Create another user 
  user2 = create_user("Ahmed", "ahmed")

  # Create server
  server = create_server("AgeDB")

  # Join server
  join_server(user1.properties["id"], server.properties["id"])

  # Send message to user
  send_message_to(user1.properties["id"], user2.properties["id"], "User", "Hello Ahmed!")
  send_message_to(user1.properties["id"], user2.properties["id"], "User", "Hello Ahmed 2!")

  # Send message to server
  send_message_to(user1.properties["id"], server.properties["id"], "Server", "Hello Server!")

  # Get messages of user
  user1_messages = get_messages_of(user1.properties["id"])
  
  # Print messages of user
  for message in user1_messages:
      print(message.toJson())