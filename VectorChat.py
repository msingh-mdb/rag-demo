''''
Select the use case you would like to execute
Comment out one of the below
'''
#import moviesSettings as settings
import airbnbSettings as settings


###########################
import json
import boto3
from botocore.exceptions import ClientError
import re
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
import os
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.environ["MONGO_URI"]
class QueryProcessor:
    """A class to process user queries using vector search and Claude LLM via Bedrock.
    
    Manages configuration, MongoDB Atlas vector search, and AWS Bedrock interactions
    to retrieve and aggregate facts based on user questions.
    """

    def __init__(self):
        """Initializes the QueryProcessor with configuration from settings.py.
        
        Sets up Bedrock and MongoDB clients, and connects to the vector collection.
        """
        # Initialize AWS Bedrock client for embeddings and LLM
        self.bedrock_client = self._create_bedrock_client()
        # Initialize MongoDB client for vector search
        self.mongo_client = self._create_mongo_client()
        # Connect to the MongoDB collection for vectorized data
        self.collection = self._get_vector_collection()
        # Conversation history (starts empty)
        self.history = None

    def _create_bedrock_client(self) -> boto3.client:
        return boto3.client(
            'bedrock-runtime',
            region_name=settings.aws_region
        )

    def _create_mongo_client(self) -> MongoClient:
        # Connect to MongoDB Atlas using the URI and Server API version 1 MongoURI
        return MongoClient(MONGO_URI, server_api=ServerApi('1'))

    def _get_vector_collection(self) -> Collection:
        database = self.mongo_client[settings.monogo_database]
        return database[settings.vector_collection]

    def generate_embedding(self, text: str) -> list:
        """Generates an embedding for the input text using the given model.
        
        Args:
            text: Input text to embed.
        
        Returns:
            list: Embedding vector (list of floats) produced by the model.
            duration: response time to generate embeddings
        """
        body = json.dumps({"inputText": text})
        # Response time calc start
        start_time = time.time()
        # Invoke the Bedrock embedding model (e.g., Titan Embeddings) specified in config
        response = self.bedrock_client.invoke_model(
            modelId=settings.EMBEDDING_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        #Response time calc stop
        duration = time.time() - start_time
        # Parse the response and extract the embedding vector
        return json.loads(response["body"].read())["embedding"], duration

    def search_similar_documents(self, query_vector: list, filters: list = None, limit: int = 100, candidates: int = 1000) -> list:
        """Performs a vector search in MongoDB Atlas to find similar documents.
        
        Args:
            query_vector: Query embedding vector to search with.
            filters: List of (key, value) tuples for metadata pre filtering (default: None).
            limit: Maximum number of results to return (default: 100).
            candidates: Number of candidate documents to consider (default: 1000).
        
        Returns:
            list: List of json strings combining chunk text and metadata for each result.
            duration: response time to perform vector search
        """
        proj_add = {}
        match_filter = {}
        # Apply filters to narrow the search if provided
        if len(filters)>0:
            print(filters)
            if len(filters) > 1:
                # Use $and for multiple filters
                match_filter = {"$and": []}
                for key, value in filters:
                    match_filter["$and"].append({key: value})
                    proj_add.update({key: 1})
            else:
                # Single filter case
                key, value = filters[0]
                match_filter={key: value}
                proj_add.update({key: 1})
        
        proj_add.update(settings.project_results)

        # Define the MongoDB Atlas vector search pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": settings.vector_index,  # Name of the vector index
                    "path": settings.vector_field,        # Field storing embeddings
                    "queryVector": query_vector, # Vector to compare against
                    "limit": limit,             # Max results to return
                    "numCandidates": candidates # Number of candidates to evaluate
                }
            },
            {
                "$project": proj_add
            }
        ]

        pipeline[0]["$vectorSearch"]["filter"] = match_filter
           

        #print(f"\n Pipeline used was: \n{pipeline} \n")
        # Execute the vector search aggregation
        # Response Time Calc start
        start_time = time.time()
        results = self.collection.aggregate(pipeline)
        # Response Time Calc stop
        duration = time.time() - start_time
        output = []
        # Combine chunk text and metadata into a single string for each result
        for result in results:
            output.append(f"{str(result)}\n")
            #output.append(f"Price: {result['price']}\nName: {result['name']}\nType: {result['property_type']}\nSummary: {result['summary']}\nAccess: {result['access']}\nScore: {result['score']}")
        
        return output, duration

    def _invoke_claude(self, prompt: str) -> tuple:
        """Sends a prompt to Claude via Bedrock and updates conversation history.
        
        Args:
            prompt: User prompt to send to the LLM.
        
        Returns:
           assistant message (str)
           duration: LLM to response time   
        """
        # Initialize history if not provided
        if self.history is None:
            self.history = []
        
        # Add the user prompt to the conversation history
        self.history.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

        # Prepare the request body for Claude's Messages API
        body = json.dumps({
            "messages": self.history,       # Full conversation history
            "anthropic_version": "bedrock-2023-05-31",  # Bedrock-specific version
            "max_tokens": 1000,            # Max output tokens
            "top_k": 250,                  # Sampling diversity parameter
            "temperature": 1,              # Randomness in response generation
            "top_p": 0.999                 # Cumulative probability for token selection
        })

        # Response Time Calc start
        start_time = time.time()
        
        # Invoke the Claude model specified in config
        response = self.bedrock_client.invoke_model(
            modelId=settings.LLM_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        # Response Time Calc stop
        duration = time.time() - start_time
        # Decode and parse the response
        response_body = response["body"].read().decode('utf-8')
        assistant_message = json.loads(response_body)["content"][0]["text"]
        # Add the assistant's response to the history
        self.history.append({"role": "assistant", "content": [{"type": "text", "text": assistant_message}]})

        return assistant_message, duration

    def extract_filters(self, question: str) -> list:
        """Extracts metadata filters from a user question using regex patterns.
            This will be specific to the data in the vector collection. For this dataset we have member_id and field in the metadata section
        
        Args:
            question: User question to analyze.
        
        Returns:
            list: List of (key, value) tuples for filtering, or None if no filters found.
        """

        # Define the regular expression pattern to capture both quoted strings and unquoted values
        # "([^"]+)" - Quoted text/numbers \d+(?:\.\d+ - int/float \w+ unquoted text (3 patterns) 
        pattern = r'(\w+)=(?:"([^"]+)"|(\d+(?:\.\d+)?)|(\w+))'
        # Remove filters from the question 
        cleanthis = r'(\w+)=(?:"([^"]+)"\s?|(\d+(?:\.\d+)\s?)|(\w+)\s?)'
        q1 = re.sub(cleanthis, '', question)

        # Find all matches for the pattern in the text
        matches = re.findall(pattern, question)
        
        # Create a list to store the captured variables and their values
        captured_values = []
        
        # Iterate over the matches and store them in the dictionary
        for match in matches:
            variable_name, quoted_value, numeric_value, unquoted_text = match
            if variable_name in settings.fields_filter:
                # Determine whether the value is a quoted string, numeric, or unquoted text
                if quoted_value:
                    captured_values.append((variable_name, quoted_value))
                elif numeric_value:
                    # Convert the numeric value to the appropriate type
                    if '.' in numeric_value:
                        captured_values.append((variable_name, {'$gte': float(numeric_value)}))
                    else:
                        captured_values.append((variable_name, {'$gte': int(numeric_value)}))
                elif unquoted_text:
                    captured_values.append((variable_name, unquoted_text))
        return captured_values, q1

    def query_claude(self, question: str, history: list or None = None) -> tuple:
        """Formats a question with optional context and sends it to Claude.  This is stateless in case we're calling from an API.
            The history would be stored in browser perhaps?
        
        Args:
            question: User question or full prompt 
            history: optional list of historical questions and assistant answers. overwrites internal history   
        
        Returns:
            tuple: (assistant response (str), updated history (list))
            duration: LLM to response time   
        """
        # update history
        if history:
            self.history = history
        # Invoke Claude with the formatted prompt
        assistant_message, duration = self._invoke_claude(question)
        return assistant_message, self.history, duration

    def retrieve_aggregate_facts(self, question: str, history: list or None = None) -> tuple:
        """Processes a user question to retrieve and aggregate facts using vector search and LLM. This is stateless in case we're calling from an API.
            The history would be stored in browser perhaps?
        
        Args:
            question: User question to process.
            history: optional list of historical questions and assistant answers. overwrites internal history
        
        Returns:
            tuple: (LLM response (str), updated history (list))
        """
        # Measure time for extracting filters
        start_time = time.time()
        filters,cleanQ = self.extract_filters(question)
        duration = time.time() - start_time
        print(f"extract_filters completed in {duration:.4f} seconds.")
        print(f"clean question: {cleanQ}")

        # Generate embedding for the question
        #start_time = time.time()
        query_vector, duration = self.generate_embedding(cleanQ)
        #duration = time.time() - start_time
        print(f"generate_embedding completed in {duration:.4f} seconds.")
        #print(f"Vector Embeddings: \n {query_vector}\n")

        # Perform vector search with fixed limits
        
        # we can probably lower this based on filters... leaving it for now
        limit = settings.NumOfResults     # Maximum results to return
        candidates = 3000  # Number of candidates to evaluate
        #start_time = time.time()
        results, duration = self.search_similar_documents(query_vector, filters, limit, candidates)
        #duration = time.time() - start_time
        print(f"search_similar_documents completed in {duration:.4f} seconds.")

        # Default response if no results are found
        response_message = "no context from vectors"
        if results:
            print(f"Results from DB: {len(results)}\n{json.dumps(results, indent=4)}")
            # Combine vector results into a single context string
            context = "\n".join(results)
            # Query Claude with the question and vector search results as context 
            #start_time = time.time()
            try:
                # Format the prompt with question and context if provided, otherwise just the question
                prompt = question if context is None else f"Question: {question}\nContext: {context}\n {settings.prompt_ask}"        
                response_message, htemp, duration = self.query_claude(prompt, history) # don't need history here
            except ClientError as error:
                # Handle AWS Bedrock errors
                error_code = error.response['Error']['Code']
                if error_code == 'ValidationException':
                    # Clear history if input exceeds token limit
                    self.history = None
                    print("too much history, clearing...", error)
                else:
                    # Log other errors without modifying history
                    print("Some other client error occurred:", error)
            #duration = time.time() - start_time
            print(f"query_claude completed in {duration:.4f} seconds.")

        return response_message, self.history

    def run(self) -> None:
        """Runs an interactive loop on the command line to handle user questions.
        
        Supports direct Claude queries (prefixed with 'ask') or vector-backed fact retrieval.
        """
        print("Enter questions (Press Ctrl+C to stop):")
        try:
            while True:
                # Get user input and strip whitespace
                user_input = input("Question: ").strip()
                answer = "unknown"  # Default answer if no processing occurs
                if user_input.startswith("ask"):
                    # Direct Claude query without vector search
                    user_input = user_input.removeprefix("ask").strip()
                    answer, history, duration= self.query_claude(user_input) # don't need histroy here, but we would need to return it for a stateless API
                    print(f"Direct 'ask' query_claude completed in {duration:.4f} seconds.")
                else:
                    # Full query with vector search and Claude
                    answer, history = self.retrieve_aggregate_facts(user_input) # don't need histroy here, but we would need to return it for a stateless API
                print("--------------------------")
                print(f"Answer: {answer}")
                print("--------------------------")
        except KeyboardInterrupt:
            # Handle user interruption
            print("\nKeyboard interrupt received, exiting...")

def main():    
    processor = QueryProcessor()
    processor.run()

if __name__ == "__main__":
    main()