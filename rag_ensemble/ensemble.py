import faiss
import numpy as np
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class RAGEnsemble:
    def __init__(self, retriever, generator, max_daily_tokens):
        self.retriever = retriever
        self.generator = generator
        self.max_daily_tokens = max_daily_tokens
    
    def add_document(self, ):
        if self.get_current_token_count() > self.max_daily_tokens:
            return Messages.EXCEEDS_MAX_TOKEN

        context = self.retriever.get_context(query)
        response = self.generator.get_response(
            instructions, query, context, history
        )
        self.log_tokens(self, results)
        return response.content
    
    def generate_response(self, instructions, query, history):
        if self.get_current_token_count() > self.max_daily_tokens:
            return Messages.EXCEEDS_MAX_TOKEN

        context = self.retriever.get_context(query)
        response = self.generator.get_response(
            instructions, query, context, history
        )
        self.log_tokens(self, results)
        return response.content

    def get_current_token_count():
        try:
            daily_calls_sum = get_daily_calls(f"{log_path}/call_log_{datetime.now().strftime('%Y-%m-%d')}.log")
        except FileNotFoundError:
            daily_calls_sum = 0
            logger.remove()
            logger.add(log_file, rotation="1 day", format="{time} {message}", level="INFO")
        return daily_calls_sum


    def log_tokens(self, results):
        result_tokens = token_counter([results],default_model)
        print(f"Prompt tokens: {token_count}")
        print(f"Completion tokens: {result_tokens}")
        total_tokens = token_count+result_tokens
        print(f"Total tokens: {total_tokens}")

        # Log statistics
        query_statistics = [token_count, result_tokens, total_tokens, 1]
        query_statistics = default_model+","+",".join(str(i) for i in query_statistics)+ " " + str(daily_calls_sum+1) 
        logger.info(query_statistics)

    