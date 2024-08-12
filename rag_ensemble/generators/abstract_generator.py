
class OpenAIGenerator(AbstractGenerator):
    def __init__(self, temperature, model_name, instructions):
        self.temperature = temperature
        self.model_name = model_name
        self.instructions = instructions
        self.chat = ChatOpenAI(temperature=temperature, model_name=model_name)

    def get_messages(self, )

    def get_response(self, query, context, history):
        self.chat(chat(messages))
        # Combine instructions + context to create system instruction for the chat model
        system_instruction = self.instructions + context

        # Convert message history to list of message objects
        messages_history = []
        i = 0
        for message in history:
            if i % 2 == 0: 
                messages_history.append(HumanMessage(content=message))
            else:
                messages_history.append(AIMessage(content=message))
            i += 1
        
        # Initialize message list
        messages = [SystemMessage(content=system_instruction)]
        for message in messages_history:
            messages.append(message)
        messages.append(HumanMessage(content=query))


    