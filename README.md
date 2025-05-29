# rag-demo

This repo is created to with the sole purpose of demoing how mongodB can be used as vector database.

# Use case
There are 3 use case:
1. Airbnb Listing
2. mflix movies
3. 10k Filings for (JPMC and Citi)

Preset dataset for mflix and airbnb can be download from the link below:<br>
[Airbnb & Mflix Collections](https://drive.google.com/file/d/1BKow5HrhxGFGvcbHEqh3FOoYM5noqK1a/view?usp=sharing) 
<br>
10K filing, I have used 2024 filling for both the banks and chunked the data into a collection:
[10K Collection](https://drive.google.com/file/d/10pi0k-DxVfsycEpxBOeXqyiCzCuK-vvx/view?usp=sharing)

# Embedding Model and LLM used
Script uses AWS bedrock [titan embedding model v2](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) 1024 demensions, and float embeddings. [Claude3 Haiku V1 LLM](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_Converse_AnthropicClaude_section.html) is used for summarization.

> [!WARNING]
> Embedding in the database and user question should have same number dimensions (1024 in this case)

# Pre-req
Load dataset into your MongoDB instance

# Directory Structure
 :file_folder: vector-index : contains vector index for that can be used for Airbnb and mflix <br>
 airbnbSettings.py -- contains pre-configured settings for sample-airbnb dataset (download dataset from above provided link)
 moviesSettings.py -- contains pre-configured settings for sample-mflix dataset (download dataset from above provided link)
 pdfSettings.py -- contains pre-configured settings for 10K filing dataset (download dataset from above provided link)
 > [!NOTE]
 > If you plan to use filters, add them to index and update filter_fields array in Settings files listed above
 
 ## Environment variables (.env)
 `MONGO_URI` MongoDB connection string 
 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` for your AWS account 
 

 VectorChat.py -- is the main script used for demo
> [!CAUTION]
> Depending on which use case you are running update import settings file.

`import moviesSettings as settings`  when demostrating movies use case<br>
`import airbnbSettings as settings`  when demoing airbnb use case<br>
`import pdfSettings as settings` when demoing 10K filing use case<br>
**`# comment out the use case you are not working with`**


# Usage example  
1. [Movies](##With-moviesSettings.py-(mflix-sample))
2. [Airbnb](##With-airbnbSetting.py-(airbnb-sample))
3. [10K Filing](##With-pdfSettings.py-(10K-filing-sample))


## With moviesSettings.py (mflix sample)
### Question without filters `show me all moveis with train robbery`
> [!NOTE]
> Spelled movies incorrectly (highlight it you would like)
<pre>
Enter questions (Press Ctrl+C to stop):
Question: show me all moveis with train robbery
extract_filters completed in 0.0011 seconds.
clean question: show me all moveis with train robbery
generate_embedding completed in 0.5708 seconds.
search_similar_documents completed in 2.5590 seconds.
Results from DB: 5
[
    "{'plot': \"A dramatization of the Great Train Robbery. While not a 'how to', it is very detail dependent, showing the care and planning that took place to pull it off.\", 'runtime': 110, 'title': 'Robbery', 'year': 1967, 'type': 'movie', 'score': 0.7608767747879028}\n",
    "{'plot': 'In Victorian England, a master criminal makes elaborate plans to steal a shipment of gold from a moving train.', 'runtime': 110, 'rated': 'PG', 'title': 'The Great Train Robbery', 'year': 1978, 'type': 'movie', 'score': 0.7337297797203064}\n",
    "{'plot': 'In this violent spaghetti western a murderous robber hijacks a payroll train, murders everyone aboard and then stashes his loot. A gunslinger learns about it and decides he wants the money ...', 'runtime': 109, 'rated': 'PG-13', 'title': 'Blood River', 'year': 1967, 'type': 'movie', 'score': 0.7302441000938416}\n",
    "{'plot': 'Multi-genre flick (western, martial arts, comedy, adventure, etc.) with an all-star cast about a man who returns to his home town, buys everything in sight, and tries to improve its ...', 'runtime': 98, 'rated': 'PG-13', 'title': 'Shanghai Express', 'year': 1986, 'type': 'movie', 'score': 0.7088623642921448}\n",
    "{'year': 1974, 'plot': \"In New York, armed men hijack a subway car and demand a ransom for the passengers. Even if it's paid, how could they get away?\", 'rated': 'R', 'title': 'The Taking of Pelham One Two Three', 'type': 'movie', 'runtime': 104, 'score': 0.7085707187652588}\n"
]
query_claude completed in 5.9750 seconds.
--------------------------
Answer: Based on the context provided, here are the movies related to train robbery:

1. Robbery (1967)
   - Plot: A dramatization of the Great Train Robbery, showing the care and planning that went into pulling it off.
   - Runtime: 110 minutes
   - Score: 0.7608767747879028

2. The Great Train Robbery (1978)
   - Plot: In Victorian England, a master criminal makes elaborate plans to steal a shipment of gold from a moving train.
   - Runtime: 110 minutes
   - Rated: PG
   - Score: 0.7337297797203064

3. Blood River (1967)
   - Plot: In this violent spaghetti western, a murderous robber hijacks a payroll train, murders everyone aboard, and then stashes the loot. A gunslinger learns about it and decides he wants the money.
   - Runtime: 109 minutes
   - Rated: PG-13
   - Score: 0.7302441000938416

4. Shanghai Express (1986)
   - Plot: A multi-genre flick (western, martial arts, comedy, adventure, etc.) with an all-star cast about a man who returns to his home town, buys everything in sight, and tries to improve it.
   - Runtime: 98 minutes
   - Rated: PG-13
   - Score: 0.7088623642921448

5. The Taking of Pelham One Two Three (1974)
   - Plot: In New York, armed men hijack a subway car and demand a ransom for the passengers. Even if it's paid, how could they get away?
   - Runtime: 104 minutes
   - Rated: R
   - Score: 0.7085707187652588

Conclusion:
The context provided clearly indicates that the question is asking for movies with a train robbery theme. The movies listed above fit this criteria, with plots involving various types of train robberies, such as the Great Train Robbery, a payroll train hijacking, and a subway car hijacking.

The movies cover a range of genres, including westerns, action, and crime dramas, and span different time periods, from the Victorian era to the 1970s. The runtimes of the movies are also relatively similar, ranging from 98 to 110 minutes.

Overall, the movies presented provide a good overview of the train robbery genre, with each film offering a unique take on the theme. The context and information provided should be sufficient to answer the original question.
--------------------------
Question: ^C
Keyboard interrupt received, exiting...
</pre>

### Question without filters `show me all moveis with train robbery runtime=100 year=1970`

> [!NOTE]
> Filter does not work well on floating or decimal field type. For numbers it will use $gte (>=).
<pre>
Enter questions (Press Ctrl+C to stop):
Question: show me all moveis with train robbery runtime=100 year=1970
extract_filters completed in 0.0009 seconds.
clean question: show me all moveis with train robbery 
generate_embedding completed in 0.6132 seconds.
[('runtime', {'$gte': 100}), ('year', {'$gte': 1970})]
search_similar_documents completed in 3.7098 seconds.
Results from DB: 5
[
    "{'plot': 'In Victorian England, a master criminal makes elaborate plans to steal a shipment of gold from a moving train.', 'runtime': 110, 'rated': 'PG', 'title': 'The Great Train Robbery', 'year': 1978, 'type': 'movie', 'score': 0.717418372631073}\n",
    "{'year': 1974, 'plot': \"In New York, armed men hijack a subway car and demand a ransom for the passengers. Even if it's paid, how could they get away?\", 'rated': 'R', 'title': 'The Taking of Pelham One Two Three', 'type': 'movie', 'runtime': 104, 'score': 0.6999773383140564}\n",
    "{'plot': 'A vengeful New York transit cop decides to steal a trainload of subway fares; his foster brother, a fellow cop, tries to protect him.', 'runtime': 110, 'rated': 'R', 'title': 'Money Train', 'year': 1995, 'type': 'movie', 'score': 0.6960840225219727}\n",
    "{'year': 2009, 'plot': \"Armed men hijack a New York City subway train, holding the passengers hostage in return for a ransom, and turning an ordinary day's work for dispatcher Walter Garber into a face-off with the mastermind behind the crime.\", 'rated': 'R', 'title': 'The Taking of Pelham 1 2 3', 'type': 'movie', 'runtime': 106, 'score': 0.6876696348190308}\n",
    "{'plot': 'On a train in 1945 a train conductor is in charge of a motley bunch: a failed author who means well but creates chaos; a soldier who is actually on the wrong train; a doctor who wants to ...', 'runtime': 100, 'title': 'Illusive Tracks', 'year': 2003, 'type': 'movie', 'score': 0.6709451079368591}\n"
]
query_claude completed in 4.9819 seconds.
--------------------------
Answer: Based on the question and the provided context, here are the movies that match the criteria:

1. The Great Train Robbery (1978)
   - Plot: "In Victorian England, a master criminal makes elaborate plans to steal a shipment of gold from a moving train."
   - Runtime: 110 minutes
   - Year: 1978

The context provided does not include any movies with a runtime of 100 minutes and a release year of 1970 related to train robberies. The closest match is "Illusive Tracks" from 2003, but it does not fit the exact criteria given in the question.

Conclusions:
- The question cannot be fully answered with the provided context, as there are no movies that match the criteria of "runtime=100" and "year=1970" for a train robbery plot.
- The context includes several movies related to train robberies or heists, such as "The Great Train Robbery" (1978) and "The Taking of Pelham One Two Three" (1974 and 2009), but they do not match the specific parameters given in the question.

To fully address the question, more information or a broader set of movie data would be needed to find any potential matches for the given criteria.
--------------------------
</pre>

## With airbnbSetting.py (airbnb sample)

### Question without filters `show me all listing in AU that water facing`
> [!NOTE]
> Intentional typos and AU used for Australia
<pre>
Enter questions (Press Ctrl+C to stop):
Question: show me all listing in AU that water facing
extract_filters completed in 0.0010 seconds.
clean question: show me all listing in AU that water facing
generate_embedding completed in 0.4877 seconds.
search_similar_documents completed in 1.3479 seconds.
Results from DB: 5
[
    "{'name': 'Water View 2 Bedroom Apartment', 'summary': 'This is a fully self contained two bedroom apartment with water views, located right in the heart of the Sydney business district and in close proximity to Darling Harbour and Town Hall.', 'access': 'Security access to building Outdoor heated resort style swimming pool and Gym', 'property_type': 'Apartment', 'price': Decimal128('259.00'), 'score': 0.6783467531204224}\n",
    "{'name': 'Ocean Views & Private Access to Beach', 'summary': 'Amazingly light and airy apartment with ocean views.  Large open plan lounge and dining space with full height windows creating a beautifully open, light and relaxing space.  Opening onto a wrap around balcony perfect for a morning coffee or afternoon BBQ. Hear the sound of the ocean from both bedrooms at night for the perfect sleep.', 'access': 'You will have access to the entire apartment. There is a lift up to the apartment.', 'property_type': 'Apartment', 'price': Decimal128('380.00'), 'score': 0.6723577976226807}\n",
    "{'name': '2 Bedroom -guest parking.', 'summary': 'Fab Cool Clean 2bd with Mod cons. Unlimited Wi-Fi, Fetch TV and Netflix. Freshwater Village and beach around the corner. Bus stop to Manly/City on doorstep. BBQ & table chairs outside. Body board & bike.', 'access': 'Queen bedroom - bathroom and kitchen/laundry', 'property_type': 'Apartment', 'price': Decimal128('100.00'), 'score': 0.661689817905426}\n",
    "{'name': 'Private Luxury Apartment Sitting atop Pittwater', 'summary': 'Escape to a beautifully located modern design apartment with a private pool and sauna. Scan the panoramic views above Pittwater from an open walk-out living room, or head down to the water to watch the boats before sunset.', 'access': 'Guest access is private', 'property_type': 'House', 'price': Decimal128('181.00'), 'score': 0.651874303817749}\n",
    "{'name': 'Whale Beach Sensation', 'summary': 'A superb modern 6 bedroom home spanning three levels with fabulous ocean views. Seven minutes walk to the beach and perfectly positioned in a quiet street.', 'access': '', 'property_type': 'House', 'price': Decimal128('1200.00'), 'score': 0.6483761072158813}\n"
]
query_claude completed in 7.6208 seconds.
--------------------------
Answer: Certainly! Here's the context provided in an easy-to-consume format:

1. Water View 2 Bedroom Apartment
   - Summary: This is a fully self-contained two-bedroom apartment with water views, located in the heart of the Sydney business district and close to Darling Harbour and Town Hall.
   - Access: Security access to the building, outdoor heated resort-style swimming pool, and gym.
   - Property Type: Apartment
   - Price: $259.00

2. Ocean Views & Private Access to Beach
   - Summary: Amazingly light and airy apartment with ocean views. Large open-plan lounge and dining space with full-height windows, opening onto a wrap-around balcony perfect for a morning coffee or afternoon BBQ. You can hear the sound of the ocean from both bedrooms at night.
   - Access: You will have access to the entire apartment, and there is a lift up to the apartment.
   - Property Type: Apartment
   - Price: $380.00

3. 2 Bedroom -guest parking.
   - Summary: Fab Cool Clean 2bd with Mod cons. Unlimited Wi-Fi, Fetch TV, and Netflix. Freshwater Village and beach around the corner. Bus stop to Manly/City on the doorstep. BBQ & table chairs outside. Body board & bike.
   - Access: Queen bedroom - bathroom and kitchen/laundry.
   - Property Type: Apartment
   - Price: $100.00

4. Private Luxury Apartment Sitting atop Pittwater
   - Summary: Escape to a beautifully located modern design apartment with a private pool and sauna. Scan the panoramic views above Pittwater from an open walk-out living room, or head down to the water to watch the boats before sunset.
   - Access: Guest access is private.
   - Property Type: House
   - Price: $181.00

5. Whale Beach Sensation
   - Summary: A superb modern 6-bedroom home spanning three levels with fabulous ocean views. Seven minutes walk to the beach and perfectly positioned in a quiet street.
   - Access: Not provided.
   - Property Type: House
   - Price: $1,200.00

Summarizing the context shared:
The provided context includes details about five different properties in Australia, all of which have some form of water view or access. The properties range from two-bedroom apartments to a six-bedroom house, with prices varying from $100 to $1,200 per night.

Conclusions based on the question and context:
The question asked to show all listings in AU that have a water facing view. The context provided appears to include all such listings, as each property has either a water view or private access to a beach or water body.

No further context is needed to answer the question, as the provided information is sufficient to identify the properties that meet the criteria of having a water-facing view.
--------------------------
</pre>

### Question without filters `show me all listing in AU that water facing sort by price low to high`

> [!IMPORTANT]
> Sort is not happening in the Database but Claude (LLM) will do it for us.
<pre>
Question: show me all listing in AU that water facing sort by price low to high
extract_filters completed in 0.0001 seconds.
clean question: show me all listing in AU that water facing sort by price low to high
generate_embedding completed in 0.1271 seconds.
search_similar_documents completed in 0.1439 seconds.
Results from DB: 5
[
    "{'name': 'Ocean Views & Private Access to Beach', 'summary': 'Amazingly light and airy apartment with ocean views.  Large open plan lounge and dining space with full height windows creating a beautifully open, light and relaxing space.  Opening onto a wrap around balcony perfect for a morning coffee or afternoon BBQ. Hear the sound of the ocean from both bedrooms at night for the perfect sleep.', 'access': 'You will have access to the entire apartment. There is a lift up to the apartment.', 'property_type': 'Apartment', 'price': Decimal128('380.00'), 'score': 0.677955150604248}\n",
    "{'name': '2 Bedroom -guest parking.', 'summary': 'Fab Cool Clean 2bd with Mod cons. Unlimited Wi-Fi, Fetch TV and Netflix. Freshwater Village and beach around the corner. Bus stop to Manly/City on doorstep. BBQ & table chairs outside. Body board & bike.', 'access': 'Queen bedroom - bathroom and kitchen/laundry', 'property_type': 'Apartment', 'price': Decimal128('100.00'), 'score': 0.6713387370109558}\n",
    "{'name': 'Water View 2 Bedroom Apartment', 'summary': 'This is a fully self contained two bedroom apartment with water views, located right in the heart of the Sydney business district and in close proximity to Darling Harbour and Town Hall.', 'access': 'Security access to building Outdoor heated resort style swimming pool and Gym', 'property_type': 'Apartment', 'price': Decimal128('259.00'), 'score': 0.6646690368652344}\n",
    "{'name': 'Whale Beach Sensation', 'summary': 'A superb modern 6 bedroom home spanning three levels with fabulous ocean views. Seven minutes walk to the beach and perfectly positioned in a quiet street.', 'access': '', 'property_type': 'House', 'price': Decimal128('1200.00'), 'score': 0.6506839394569397}\n",
    "{'name': 'Beautiful 4 Bedroom House with pool', 'summary': 'My place is close to Curl Curl Beach and Freshwater Beach.  5 minute drive to Manly Beach. You\u2019ll love my place because of the outdoors space. My place is good for couples, families (with kids), and big groups.', 'access': '', 'property_type': 'Apartment', 'price': Decimal128('699.00'), 'score': 0.6498813033103943}\n"
]
query_claude completed in 6.2939 seconds.
--------------------------
Answer: Here is the context shared in an easy-to-consume format, sorted by price from low to high:

1. '2 Bedroom -guest parking.'
   - Summary: Fab Cool Clean 2bd with Mod cons. Unlimited Wi-Fi, Fetch TV and Netflix. Freshwater Village and beach around the corner. Bus stop to Manly/City on doorstep. BBQ & table chairs outside. Body board & bike.
   - Access: Queen bedroom - bathroom and kitchen/laundry
   - Property Type: Apartment
   - Price: $100.00

2. 'Water View 2 Bedroom Apartment'
   - Summary: This is a fully self-contained two-bedroom apartment with water views, located right in the heart of the Sydney business district and in close proximity to Darling Harbour and Town Hall.
   - Access: Security access to building, outdoor heated resort-style swimming pool, and gym
   - Property Type: Apartment
   - Price: $259.00

3. 'Ocean Views & Private Access to Beach'
   - Summary: Amazingly light and airy apartment with ocean views. Large open-plan lounge and dining space with full-height windows, opening onto a wrap-around balcony perfect for a morning coffee or afternoon BBQ. You can hear the sound of the ocean from both bedrooms at night.
   - Access: You will have access to the entire apartment, and there is a lift up to the apartment.
   - Property Type: Apartment
   - Price: $380.00

4. 'Beautiful 4 Bedroom House with pool'
   - Summary: My place is close to Curl Curl Beach and Freshwater Beach. 5 minute drive to Manly Beach. You'll love my place because of the outdoors space. My place is good for couples, families (with kids), and big groups.
   - Access: Not provided
   - Property Type: Apartment
   - Price: $699.00

5. 'Whale Beach Sensation'
   - Summary: A superb modern 6-bedroom home spanning three levels with fabulous ocean views. Seven minutes walk to the beach and perfectly positioned in a quiet street.
   - Access: Not provided
   - Property Type: House
   - Price: $1,200.00

Summarizing the context shared:
The provided context includes details about five different properties in Australia, all of which have some form of water view or access. The properties range from two-bedroom apartments to a six-bedroom house, with prices varying from $100 to $1,200 per night.

Conclusions based on the question and context:
The question asked to show all listings in AU that have a water-facing view, sorted by price from low to high. The context provided includes the necessary information to fulfill this request.

The results are presented in the order of increasing price, starting from the lowest-priced property ($100 per night) to the highest-priced property ($1,200 per night). All the properties listed have either a water view or private access to a beach or water body.

No further context is needed to answer the question, as the provided information is sufficient to identify the properties that meet the criteria and present them in the requested order.
--------------------------
</pre>

### Question without filters `show me all listing in AU that water facing sort by price low to high bedrooms=2 bathroom=1`

> [!NOTE]
> Filter does not work well on floating or decimal field type. For numbers it will use $gte (>=).

<pre>
Question: show me all listing in AU that water facing sort by price low to high bedrooms=2 bathroom=1
extract_filters completed in 0.0001 seconds.
clean question: show me all listing in AU that water facing sort by price low to high 
generate_embedding completed in 0.1983 seconds.
[('bedrooms', {'$gte': 2})]
search_similar_documents completed in 0.3664 seconds.
Results from DB: 5
[
    "{'name': 'Ocean Views & Private Access to Beach', 'summary': 'Amazingly light and airy apartment with ocean views.  Large open plan lounge and dining space with full height windows creating a beautifully open, light and relaxing space.  Opening onto a wrap around balcony perfect for a morning coffee or afternoon BBQ. Hear the sound of the ocean from both bedrooms at night for the perfect sleep.', 'access': 'You will have access to the entire apartment. There is a lift up to the apartment.', 'property_type': 'Apartment', 'bedrooms': 2, 'price': Decimal128('380.00'), 'score': 0.6750421524047852}\n",
    "{'name': '2 Bedroom -guest parking.', 'summary': 'Fab Cool Clean 2bd with Mod cons. Unlimited Wi-Fi, Fetch TV and Netflix. Freshwater Village and beach around the corner. Bus stop to Manly/City on doorstep. BBQ & table chairs outside. Body board & bike.', 'access': 'Queen bedroom - bathroom and kitchen/laundry', 'property_type': 'Apartment', 'bedrooms': 2, 'price': Decimal128('100.00'), 'score': 0.6681163311004639}\n",
    "{'name': 'Water View 2 Bedroom Apartment', 'summary': 'This is a fully self contained two bedroom apartment with water views, located right in the heart of the Sydney business district and in close proximity to Darling Harbour and Town Hall.', 'access': 'Security access to building Outdoor heated resort style swimming pool and Gym', 'property_type': 'Apartment', 'bedrooms': 2, 'price': Decimal128('259.00'), 'score': 0.6605812907218933}\n",
    "{'name': 'Beautiful 4 Bedroom House with pool', 'summary': 'My place is close to Curl Curl Beach and Freshwater Beach.  5 minute drive to Manly Beach. You\u2019ll love my place because of the outdoors space. My place is good for couples, families (with kids), and big groups.', 'access': '', 'property_type': 'Apartment', 'bedrooms': 4, 'price': Decimal128('699.00'), 'score': 0.6490702033042908}\n",
    "{'name': 'Whale Beach Sensation', 'summary': 'A superb modern 6 bedroom home spanning three levels with fabulous ocean views. Seven minutes walk to the beach and perfectly positioned in a quiet street.', 'access': '', 'property_type': 'House', 'bedrooms': 6, 'price': Decimal128('1200.00'), 'score': 0.6457250118255615}\n"
]
query_claude completed in 7.0064 seconds.
--------------------------
Answer: Here is the context shared in an easy-to-consume format, sorted by price from low to high and filtered for properties with 2 bedrooms and 1 bathroom:

1. '2 Bedroom -guest parking.'
   - Summary: Fab Cool Clean 2bd with Mod cons. Unlimited Wi-Fi, Fetch TV and Netflix. Freshwater Village and beach around the corner. Bus stop to Manly/City on doorstep. BBQ & table chairs outside. Body board & bike.
   - Access: Queen bedroom - bathroom and kitchen/laundry
   - Property Type: Apartment
   - Bedrooms: 2
   - Bathrooms: 1
   - Price: $100.00

2. 'Water View 2 Bedroom Apartment'
   - Summary: This is a fully self-contained two-bedroom apartment with water views, located right in the heart of the Sydney business district and in close proximity to Darling Harbour and Town Hall.
   - Access: Security access to building, outdoor heated resort-style swimming pool, and gym
   - Property Type: Apartment
   - Bedrooms: 2
   - Bathrooms: 1
   - Price: $259.00

3. 'Ocean Views & Private Access to Beach'
   - Summary: Amazingly light and airy apartment with ocean views. Large open-plan lounge and dining space with full-height windows, opening onto a wrap-around balcony perfect for a morning coffee or afternoon BBQ. You can hear the sound of the ocean from both bedrooms at night.
   - Access: You will have access to the entire apartment, and there is a lift up to the apartment.
   - Property Type: Apartment
   - Bedrooms: 2
   - Bathrooms: 1
   - Price: $380.00

Summarizing the context shared:
The provided context includes details about three different properties in Australia, all of which have some form of water view or access, and meet the criteria of having 2 bedrooms and 1 bathroom. The properties range in price from $100 to $380 per night.

Conclusions based on the question and context:
The question asked to show all listings in AU that have a water-facing view, sorted by price from low to high, and filtered for properties with 2 bedrooms and 1 bathroom. The context provided includes the necessary information to fulfill this request.

The results are presented in the order of increasing price, starting from the lowest-priced property ($100 per night) to the highest-priced property ($380 per night). All the properties listed have either a water view or private access to a beach or water body, and meet the criteria of having 2 bedrooms and 1 bathroom.

No further context is needed to answer the question, as the provided information is sufficient to identify the properties that meet the criteria and present them in the requested order.
--------------------------
</pre>
 
## With pdfSettings.py (10K filing sample)
### Question specific to JPMC using filters `how are the macro economic conditions impacting banking sector? metadata.author="JPMC"`

<pre>
 Enter questions (Press Ctrl+C to stop):
Question: how are the macro economic conditions impacting banking sector? metadata.author="JPMC"      
extract_filters completed in 0.0009 seconds.
clean question: how are the macro economic conditions impacting banking sector? 
generate_embedding completed in 0.4304 seconds.
[('metadata.author', 'JPMC')]
search_similar_documents completed in 0.4059 seconds.
Number of results from DB: 20
query_claude completed in 7.3822 seconds.
--------------------------
Answer: The provided context discusses how macroeconomic conditions are impacting the banking sector, specifically JPMorgan Chase (JPMC). The key points are:

1. Adverse economic conditions can lead to:
   - Increase in delinquencies, additions to loan loss allowances, and higher net charge-offs, reducing JPMC's earnings.
   - Worse impacts in certain geographies with declining industries or high consumer debt levels.
   - Negative effects on JPMC's consumer businesses from government policies and actions that affect consumers.

2. Unfavorable market and economic conditions can adversely affect JPMC's wholesale businesses:
   - Reduced transaction volumes and revenue from capital markets activities like loan syndications and securities underwriting.
   - Losses from having to dispose of credit commitments at a loss or hold larger residual positions.
   - Diminished fees from managing or holding client assets due to declining asset values.

3. Specific economic changes that can impact JPMC include:
   - Contraction of available credit and widening of credit spreads.
   - Currency fluctuations, reduced investments, and disruptions to supply chains.
   - Geopolitical challenges in regions like Russia, the Middle East, and China.

4. JPMC's consumer businesses can be negatively affected by factors like:
   - Personal and household income distribution, unemployment, interest rate changes, and changes in the value of collateral.
   - Reductions in consumer and small business confidence, and changes in consumer spending and debt levels.

5. JPMC's wholesale clients in certain sectors, like commercial real estate, can be impacted by economic downturns, leading to increased credit losses for JPMC.

In conclusion, the context indicates that adverse macroeconomic conditions, such as economic downturns, rising interest rates, and geopolitical instability, can have a significant negative impact on the banking sector, particularly on JPMC's consumer and wholesale businesses, leading to increased credit losses, reduced revenues, and pressure on profitability.
</pre>


### Question specific to Citi using filters `how are the macro economic conditions impacting banking sector? metadata.author="Citigroup"`

<pre>
 Question: how are the macro economic conditions impacting banking sector? metadata.author="Citigroup" 
extract_filters completed in 0.0002 seconds.
clean question: how are the macro economic conditions impacting banking sector? 
generate_embedding completed in 0.1219 seconds.
[('metadata.author', 'Citigroup')]
search_similar_documents completed in 0.1753 seconds.
Number of results from DB: 20
query_claude completed in 8.5203 seconds.
--------------------------
Answer: The context provided discusses how macroeconomic conditions are impacting the banking sector, specifically Citigroup (Citi). The key points are:

1. Macroeconomic Conditions:
   - Under Citi's base macroeconomic forecast, U.S. real GDP growth is expected to slow during 2025 and 2026, while the unemployment rate is expected to increase in 2025 but decline in 2026.
   - Citi's downside scenario assumes a recession, including an elevated average U.S. unemployment rate of 6.8% over the eight-quarter forecast period, with a peak difference of 3.4% compared to the base scenario.

2. Allowance for Credit Losses (ACL):
   - Citi's ACL is estimated using three probability-weighted macroeconomic scenarios - base, upside, and downside.
   - The ACL is sensitive to changes in the macroeconomic variables, especially the U.S. unemployment rate and real GDP growth.
   - Citi's downside scenario has more adverse macroeconomic assumptions than the base scenario, which would result in a higher ACL.

3. Impact on Citi's Businesses:
   - Higher inflation, interest rate changes, and other macroeconomic factors could negatively impact Citi's consumer and institutional clients, businesses, cost of credit, and overall results of operations.
   - Citi's net interest income could be adversely affected by a decline in interest rates or a flattening or inversion of the yield curve.

4. Sensitivity Analysis:
   - If Citi applied its downside scenario with more adverse macroeconomic assumptions, it would result in a significant increase in the ACL compared to the base scenario.
   - Citi's ACL is also impacted by qualitative factors, such as transfer risk associated with exposures outside the U.S. and potential impacts on vulnerable industries and regions.

In conclusion, the context indicates that adverse macroeconomic conditions, such as economic slowdowns, rising unemployment, and changes in interest rates, can have a significant negative impact on the banking sector, particularly on Citi's allowance for credit losses, net interest income, and overall financial performance.
--------------------------
</pre>


### Question that is not specific (no filters) `how are the macro economic conditions impacting banking sector? generate answer for each metadata.author value`

> [!IMPORTANT]
> Claude (LLM) will summarize findings bases on context provided for each metadata.author

<pre>
Question: how are the macro economic conditions impacting banking sector? generate answer for each metadata.author value
extract_filters completed in 0.0001 seconds.
clean question: how are the macro economic conditions impacting banking sector? generate answer for each metadata.author value
generate_embedding completed in 0.1704 seconds.
search_similar_documents completed in 0.2587 seconds.
Number of results from DB: 20
query_claude completed in 8.9592 seconds.
--------------------------
Answer: JPMorgan Chase (JPMC):
- Adverse economic conditions can lead to increased delinquencies, higher allowance for credit losses, and higher net charge-offs, reducing JPMC's earnings. This can be worse in certain geographies with high unemployment or consumer debt.
- JPMC's consumer businesses can be negatively affected by government policies and actions that impact consumers, such as changes to medical insurance, education, or financial services regulations.
- Unfavorable market and economic conditions can negatively impact JPMC's wholesale businesses by reducing transaction volumes and revenue from capital markets activities.
- Macroeconomic factors like credit contraction, currency fluctuations, and geopolitical events can cause JPMC to suffer losses, reduce its liquidity and capital levels, and hamper its ability to serve clients.
- JPMC's consumer businesses can be negatively affected by factors like unemployment, inflation, and changes in consumer spending and debt levels.
- Adverse economic conditions affecting specific sectors or regions can lead to increased credit losses for JPMC's clients in those areas.

Citigroup (Citi):
- Citi's base macroeconomic forecast expects U.S. real GDP growth to slow and unemployment to increase in 2025, then improve in 2026.
- Citi's downside scenario assumes a recession, with a higher average unemployment rate and GDP contraction.
- Citi's allowance for credit losses (ACL) is sensitive to macroeconomic scenarios, with the downside scenario resulting in a significantly higher ACL.
- Macroeconomic factors like inflation, interest rate changes, and geopolitical uncertainties could negatively impact Citi's businesses, cost of credit, and overall results.
- Citi's net interest income could be adversely affected by declining interest rates or a flattening/inverting yield curve.

In summary, the context indicates that adverse macroeconomic conditions, such as economic downturns, rising unemployment, changing interest rates, and geopolitical instability, can have a significant negative impact on the banking sector, affecting factors like credit quality, revenue, and profitability for both JPMC and Citi. The banks' allowances for credit losses are particularly sensitive to macroeconomic forecasts.
--------------------------
</pre>
