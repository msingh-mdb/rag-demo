###################################
# MongoDB settings
###################################
# Database name
monogo_database = "sample_airbnb" 
# Collection name to use for vector search
vector_collection = "listingsAndReviews" 
# Vector index name to use
vector_index = "Airbnb_vector" 
# Field that contains vector embeddings
vector_field = "embedding"

# Vector Search Result Projection 
project_results = {"name": 1,                
                    "property_type": 1,              
                    "summary": 1,              
                    "access" : 1,
                    "price" : 1,
                    "score": {"$meta": "vectorSearchScore"},  
                    "_id": 0 }
# Number of records to return 
NumOfResults = 5
# Fields to extract from question to filter on
fields_filter = ['bedrooms','beds','bathrooms']  
###################################
# AWS bedrock settings
###################################
aws_region="us-east-2"
#https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html
#https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModelWithResponseStream_TitanTextEmbeddings_section.html
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
#https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_Converse_AnthropicClaude_section.html
LLM_MODEL_ID = "us.anthropic.claude-3-haiku-20240307-v1:0"
prompt_ask = "Present the context shared in a easy to consume format. Summerize the context shared. Derive conclusions based on question and context shared, summarize and explain results, add further context as necessary. Avoid hallucinations."