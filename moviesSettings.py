###################################
# MongoDB settings
###################################
# Database name
monogo_database = "sample_mflix" 
# Collection name to use for vector search
vector_collection = "movies" 
# Vector index name to use
vector_index = "movies_vector" 
# Field that contains vector embeddings
vector_field = "embedding"

# Vector Search Result Projection 
project_results = {"title": 1,                
                    "year": 1,              
                    "runtime": 1,              
                    "plot" : 1,
                    "type" : 1,
                    "rated" : 1,
                    "score": {"$meta": "vectorSearchScore"},  
                    "_id": 0 }
# Number of records to return 
NumOfResults = 5
# Fields to extract from question to filter on
fields_filter = ['year','runtime']  
###################################
# AWS bedrock settings
###################################
aws_region="us-east-2"
#https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html
#https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModelWithResponseStream_TitanTextEmbeddings_section.html
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
#https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_Converse_AnthropicClaude_section.html
LLM_MODEL_ID = "us.anthropic.claude-3-haiku-20240307-v1:0"
prompt_ask = "Present the context shared in a easy to consume format. Derive conclusions based on question and context shared. Summarize and explain results, add further context as necessary. Avoid hallucinations."