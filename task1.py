def chatbot():
    print("Hello! I'm your simple chatbot. How can I assist you?")
    
    while True:
        user_input = input("You: ").lower()
        if user_input in ["hi", "hello", "hey"]:
            print("Chatbot: Hello! How can I help you today?")
        elif user_input in ["bye", "goodbye"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        elif "name" in user_input:
            print("Chatbot: I am a simple chatbot without a name, but you can call me Bot!")
        
        elif "help" in user_input:
            print("Chatbot: I'm here to assist you. Ask me anything!")
        
        elif "weather" in user_input:
            print("Chatbot: Sorry, I cannot check the weather for you, but it's always sunny with me!")
        else:
            print("Chatbot: I'm not sure how to respond to that. Can you ask something else?")
chatbot()