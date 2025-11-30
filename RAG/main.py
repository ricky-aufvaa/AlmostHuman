from chains import chain_with_message_history

def main():
    """Main function to run the RAG chatbot"""
    print("RAG Chatbot initialized. Type 'exit' to quit.")
    
    session_id = "default_session"
    
    while True:
        question = input("\nYou: ")
        
        if question.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not question.strip():
            continue
        
        try:
            response = chain_with_message_history.invoke(
                {"question": question},
                config={"configurable": {"session_id": session_id}},
            )
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
