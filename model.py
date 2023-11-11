from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from openai import OpenAI
import streamlit as st

class Evaluate:
    def __init__(self):
        self.model_path = Path('./model/EncoderModel')
        self._dataset_path = Path('./dataset')
        self.embeddings_path = self._dataset_path / 'verse_embeddings.pkl'
        #self.bible_path = self._dataset_path / 'kjv_bible.csv'
        self.bible_path = self._dataset_path / 'bsb.csv' #https://berean.bible/downloads.htm

        try:
            self._get_bible()
            self._get_embeddings()
            self._prepare_model()
        except:
            raise IOError

    def _get_embeddings(self):
        with open(self.embeddings_path,'rb') as f:
            data:dict = pickle.load(f)

        embeddings:np.ndarray = data['embeddings']
        
        self.embeddings = embeddings

    def _get_bible(self):
        self.bible = pd.read_csv(self.bible_path)

    def _prepare_model(self):
        self.model:SentenceTransformer = SentenceTransformer(str(self.model_path))
        self.model.eval()

    def _evaluate(self,text):
        text_embeddings = self.model.encode([text])
        return text_embeddings

    def get_verses(self,text,top=10):
        text_embeddings = self._evaluate(text)
        similarities = cosine_similarity(self.embeddings, text_embeddings)
        similarities = similarities.reshape(-1)
        
        indices = similarities.argsort()
        top_indices = [idx for idx in indices][::-1][:top]

        verses = self.bible.iloc[top_indices,:]
        response = {
            'reference': verses.loc[:,'reference'].tolist(),
            'verse': verses.loc[:,'text'].tolist()
        }
        return response

    
    def callChatGPT(self,query):
        #api_key = os.environ['OAIKEY']
        # Add your OPENAI API Key to Secrets in https://share.streamlit.io/
        api_key = st.secrets['OAIKEY']
        client = OpenAI(api_key=api_key)
    
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a smart Bible search tool. You provide five most appropriate Bible Verses using bullet points from the ESV Bible based on the user question or paraphrased verse. Don't provide intros, opinions or summaries"},
                {"role": "user", "content": f"{query}"}
            ]
        )
        return(completion.choices[0].message.content)


