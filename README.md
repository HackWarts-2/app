# INSTARGET🎯
INSTArget helps instagram businesses and content creators analyse and get insights about their competitors’ data and learn how to use similar strategies in order to improve their own business/profile.
## Features
  ### Competitor Analysis
  - Insights on strategies by those similar profiles on 5 latest posts
  - Deeper Insights on similar profiles on upto 50 latest posts
  ### ASK ME BOT
  - Users can query anything regarding their account category
  - Users can enter competitors url and query on aything related to their past 50 posts
###  Content Creation support
   - Instant ideas for stories, reels,posts based on users entered data
   - Users can further query and chat for as long as they want
## Tech Stack

  - Python
  - Langchain
  - Streamlit
  - Weaviate Vector Database
  - HuggingFace Embeddings
  - APIFY API



## Functionality
### Landing Page
  ![redirecting to "ASK ME" without filling forms](/screenshots/1.PNG)
### The first step
Our landing page is designed to provide first-time users with comprehensive details about how to get started with the app and the various features it offers. It includes a clear, step-by-step guide to help users navigate the initial setup and understand the functionalities available. The instructions are aimed at making the onboarding process as smooth and intuitive as possible.

Once the user clicks on the "Getting Started" button, they are redirected to the details page.
### Redirected to Details Page

Users can take two steps from here:

- **The simpler one**: Users can skip form filling and directly access our "ASK ME" RAG-chat bot to get instant insights by simply selecting their Instagram account category.
  
  We have created vector database collections of various Instagram account categories like Fashion, Beauty, Travel, Photography, Technology, and many more in the <b>Weaviate Vector Database</b>. Our <b>RAG chatbot</b> has access to these collections, and based on the user's selected category, the chatbot answers those queries using the profiles and their posts that we have stored in those category's collections. The results received are also cited by post URLs as they are already present in the vector database.
  The user can start entering their questions from here as well without adding the username as shown in the image below:
  
  <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/25.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/26.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
   </div>
   <div>The following responses were received by the <b>Falcon LLM</b>. As shown below, the referenced posts are also accessible.All generated responses include convenient links that
      enable users to verify the authenticity of the information provided. By clicking these links, users can be redirected to the relevant posts, allowing them to review the content firsthand and ensure its accuracy. 
    This feature not only enhances 
   transparency but also provides a seamless way for users to engage with the original posts and gather more detailed insights.</div> 
    <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/27.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/28.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
   </div>
   <div>Alternatively, user can also enter specific usernames-for the profiles they want to query-allowing them to get data from those profiles as well. </div>
 <p>When a user enters an Instagram account and clicks on submit, a series of backend processes are initiated to provide accurate and insightful responses. First, the <b>APIFY API</b> is used to fetch comprehensive data from the specified account. This data includes past 50 posts, and other information about the users account.
Once the data is collected, it is transformed into embeddings using <b>HuggingFace Embeddings</b>. These embeddings represent the data in a way that makes it easily searchable and analyzable. The embeddings are then stored in the <b>Weaviate Vector Database</b>.
 <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/29.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/30.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
   </div>
   The green success message indicates the successful addition of users data to the already vast database.
   
 Now,when the user queries something specific to that Instagram profile, the system searches the Weaviate Vector Database for the most relevant information. The retrieved data is used to generate a relevant detailed response.
 This process ensures that users receive precise and relevant information tailored to their specific queries as shown in the image below
   <img src="/screenshots/31.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: auto; height: 300px;"/>
<p>  As it can be seen, the chat bot clearly provided the products that are in trend as asked by the user.</p>
    
<div style="display: flex; justify-content: space-between;">
<img src="/screenshots/32.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
 <img src="/screenshots/33.PNG" alt="redirecting to 'ASK ME' without filling forms" style="width: 48%; height: 300px;"/>
   </div>
   
   
- **For More Specific Information**:
   
   In this process, users are required to provide information about the category and type of their Instagram account. This is the only mandatory information needed. Additionally, users can optionally define a subcategory, city, and country. Once all the necessary information is entered, it is stored in session storage. This data is then used to generate a query that will be sent to the <b>Google Search Engine</b> to fetch similar high-engagement accounts. The more information users provide, the better the results.

Furthermore, there is an optional username field where users can enter their existing account. If they choose to do so, the <b>APIFY API</b> fetches their past posts, which are stored and used to generate results tailored to their existing account. However, it is entirely optional and users can proceed without it as well.
<img src="/screenshots/2.PNG" alt="details page" style="width: auto; height: 300px;"/>
<p>Once the user clicks on submit, the process to get similar profiles ie the top profies matching the generated query are started being  fetched:</p>
<img src="/screenshots/3.PNG" alt="details page" style="width: auto; height: 300px;"/>
<p>As soon as the profiles are fetched, users are redirected to the "Similar Profiles" page, where they can view profiles that are similar to their own.</p>
<img src="/screenshots/4.PNG" alt="similar profile page" style="width: auto; height: 300px;"/>
<p>On<b>Smilar Profiles page</b>, user gets data of their competitors-their follower count, profile pictures, usernames urls. Moreover, to get insighst on the strategies they ahve been following lately, user gets two buttons </p>
<p>The first one, <b>Get Insights</b> lead user to a page ahving detailed insights o the strateggies they have followed on their most recent 5 posts and how users themselves can incorporate those for their own posts. Urls are also provided to the users to visit those posts on instagram</p>
<p>The page looks like this:</p>
 <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/5.PNG" alt="getting latest 5 posts" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/6.PNG" alt="redirecting to 'gettig latest 5 posts" style="width: 48%; height: 300px;"/>
       
   </div>
   <p>Secondly, <b>Ask Anything</b> lead user to a the ask me RAG chatbot and automatically ingests the selected accounts data to the vector database and enables the user to  query from their profiles till upto 50 latest posts. The user can ask anything related to what theyre doing, what theyve posted, ask for suggestions etc</p>
   
<div>
    <img src="/screenshots/7.PNG" alt="ask me bot" style="width: 48%; height: 300px;"/>
  </div>
  <div>Again,since this is the ASK ME chatboot, all the responses generated provide reference links:</div>

 <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/8.PNG" alt="getting latest 5 posts" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/9.PNG" alt="redirecting to 'getting latest 5 posts" style="width: 48%; height: 300px;"/>
       
   </div>

   <div>
Moreover, with their registered information on the details page, users can now obtain deeper insights from the ASK ME chatbot. The chatbot leverages both the user's own data and the information stored in the vector database. Once users access the ASK ME bot, their category is automatically selected, and they have the optional ability to enter another account’s username if desired.

Users can start chatting immediately about similar account categories using the RAG-based ASK ME chatbot..
     <div><img src="/screenshots/17.PNG" alt="ASK ME" style="width: auto; height: 300px;"/></div>
     This is the generated response when content related query was passed.
   <div>  <img src="/screenshots/18.PNG" alt="ASK ME" style="width: auto; height: 300px;"/></div>
   The deeper insights are clearly vsiible as the bot provides relevant hashtags and content ideas based on what the competitors have been doing.Again,they're supported by reference posts urls.
      <div>  <img src="/screenshots/19.PNG" alt="ASK ME" style="width: auto; height: 300px;"/></div>
     
   </div>
   <div>Furthermore, user can give their competitors username as well and as specific questions regarding that, as shown in the image below</div>
<div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/20.PNG" alt="ASK ME" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/21.PNG" alt="ASK ME" style="width: 48%; height: 300px;"/>
   
   </div>
   <div>The responses are as folllows: </div>
    <div> <img src="/screenshots/22.PNG" alt="ASK ME" style="width: auto; height: 300px;"/></div>
    <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/23.PNG" alt="ASK ME" style="width: 48%; height: 300px;"/>
    <img src="/screenshots/24.PNG" alt="ASK ME" style="width: 48%; height: 300px;"/>
   
   </div>
<div>Last but not least, once users enter their details, they gain access to our Content Creation Chatbot. This tool offers inspiration for reels, posts, and story ideas tailored to the information users provide. For instance, if users specify a city or country, they might receive content ideas that highlight specific locations, helping them create engaging and location-specific content.
The responses are generated by <b>Falcon LLM</b>, which employs Langchain and prompt engineering with different prompts for each type of content (stories, reels, posts). These prompts incorporate the query generated during the form submission, which is used within the prompt templates to ensure relevant and personalized suggestions.</div>
The best part is that once users click on "Generate Content," they receive instant ideas for stories, reels, and posts. For even more tailored suggestions, users can interact with the chatbot to further customize their content ideas.

 <div style="display: flex; justify-content: space-between;">
    <img src="/screenshots/10.PNG" alt="getting ideas" style="width: 38%; height: 300px;"/>
    <img src="/screenshots/11.PNG" alt="getting ideas" style="width: 38%; height: 300px;"/>
     <img src="/screenshots/12.PNG" alt="getting ideas" style="width: 38%; height: 300px;"/>  
   </div>

   <div>The following ideas were generated based on the options selected on the detailed page, as shown abovee</div>
   <div style="display: flex; justify-content: space-between;">
   <img src="/screenshots/13.PNG" alt="getting ideas" style="width: auto; "/>
   <img src="/screenshots/14.PNG" alt="getting ideas" style="width: auto; "/>
     <img src="/screenshots/15.PNG" alt="getting ideas" style="width: auto; "/>
   </div>
   <div>As observed, the generated responses are highly useful and comprehensive, meeting the needs of content creators. For instance, the reel ideas provide detailed suggestions on how to start, where to set up, and what to showcase. For posts, the tool generates captions along with hashtags and potential setups. The story ideas are also trendy, featuring engaging concepts like Q&A sessions and cooking with kids, which can be developed into a series for daily stories.</div>
</div>
 


