import os
import base64
import requests
import openai
from openai import OpenAI
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import io
import base64

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI()

def chatGPT(user_prompt:str, system_prompt: str, temperature: float, document:str='')->str:
    completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"This is the document: {document}"},
        {"role": "user", "content": f"{user_prompt}"}
    ],
    temperature = temperature,
    )
    response = completion.choices[0].message.content
    return response

def summarization(document:str, user_prompt = '', length = 'medium', format = 'paragraph'):
    temperature = 1
    system_prompt = f'''
    You will be given the content from a webpage to read.
    Please do summarization for the content.
    '''
    answer_format = ''
    if length == 'short':
        system_prompt += ' Your answer should be breif enough to guarantee that the output is less than 50 words.'
    elif length == 'medium':
        system_prompt += ' Your answer should be in moderate length with the output is less than 100 words.'
    elif length == 'long':
        system_prompt += ' Your answer should be long enough with the output is less than 250 words.'
    if format == 'paragraph':
        answer_format = 'Your answer should be writen in paragraphs. You can not use bullet point.'
    elif format == 'bullet':
        answer_format = '''
        Your answer should be listed bullet point like this
        'Summary:
        •<Write your summary here>
        •<Write your summary here>'
        '''
    system_prompt += answer_format
    summary = chatGPT(user_prompt, system_prompt, temperature, document)
    summary = summary.replace('\n', '<br>')
    return summary

def list_summarization(document:list[str], user_prompt = '', length = 'medium', format = 'paragraph'):
    summary_list = []
    # for doc in document:
    #     summary = summarization(doc, user_prompt='', length='long', format='paragraph')
    #     summary_list.append(summary)

    # system_prompt = '''
    # The user read several webpages. You will be given a list of summaries of each webpage they have viewed. Please do summarization for the list of summaries.
    # Notice that you should not do summarization separately, you need to combine all the summaries into one, which means there should be only one title 'Summary' in the generated summary. 
    # Your final answer should be a summary of all the summaries like this:
    # Summary:
    # <your answer>
    # '''
    # summaries = ''
    # for content in summary_list:
    #     summaries += content
    # summary = summarization(summaries, user_prompt, length, format)
    summary = '''
    <h1>Summary</h1>
    <h2>AI News Insights</h2>
    <Strong>Multi-Agent AI: A New Era in Software Development</Strong> Multi-agent AI systems, leveraging multiple large language models (LLMs) for specific roles, promise significant improvements in complex tasks like software development. 
    The AutoGen framework demonstrates superior performance by dividing tasks into specialized subtasks handled by different AI agents. This approach mirrors human project management and is supported by frameworks like Crew AI and LangGraph. 
    This multi-agent method optimizes performance by focusing on specific sub-tasks, enhancing efficiency and effectiveness.<br>
    <br>
    sources:<br>
    1. Multi-agent collaboration - Andrew - DeepLearning.AI <a href="https://www.deeplearning.ai/the-batch/issue-245/">Read more<a><br>
    2. The Promise of Multi-Agent AI <a href="https://www.forbes.com/sites/joannechen/2024/05/24/the-promise-of-multi-agent-ai/?sh=573e3e3a4d97">Read more<a><br>
    <br>
    <h2>Travel Insights</h2>
    <Strong>Exploring Mehrangarh Fort, Jodhpur</Strong> Mehrangarh Fort, a massive and historic fortification in Jodhpur, India, offers visitors a blend of rich history and architectural grandeur. 
    Known for its intricate carvings, expansive courtyards, and museums, the fort provides a comprehensive look into Rajasthan's royal past. 
    Key highlights include the Phool Mahal (Flower Palace), Sheesh Mahal (Mirror Palace), and the fort's impressive ramparts offering panoramic views of the city.<br>
    <br>
    sources:<br>
    1. Mehrangarh Fort, Jodhpur: The Complete Guide <a href="https://www.tripsavvy.com/mehrangarh-fort-complete-guide-4165570">Read more<a><br>
    2. Mehrangarh Fort Of Jodhpur - All You Need To Know <a href="https://www.veenaworld.com/blog/mehrangarh-fort-jodhpur">Read more<a><br>
    <br>
    <h2>Crypto Insights</h2>
    <Strong>Pros and Cons of Investing in NFTs</Strong> Investing in Non-Fungible Tokens (NFTs) presents unique opportunities and risks. 
    NFTs offer the potential for significant returns and the ability to own digital assets like art and collectibles. 
    However, the market is highly speculative, with volatility and the risk of losing value being significant concerns. 
    Investors should be aware of the regulatory environment and the challenges of liquidity in the NFT market.<br>
    <br>
    sources:<br>
    1. Pros and Cons of Investing in NFTs <a href="https://www.investopedia.com/pros-and-cons-of-investing-in-nfts-5220290">Read more<a>
    '''
    return summary, summary_list

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def tSNE(summary_list):
    num_clusters = 3
    embeddings = np.array([get_embedding(summary) for summary in summary_list])
    tsne = TSNE(n_components=2, random_state=42, perplexity=int(len(summary_list)/num_clusters))
    embeddings_2d = tsne.fit_transform(embeddings)
    embeddings_2d = (embeddings_2d - np.mean(embeddings_2d, axis=0)) / np.std(embeddings_2d, axis=0)
    return embeddings_2d

def kmeans(embeddings_2d):
    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(embeddings_2d)
    return clusters

