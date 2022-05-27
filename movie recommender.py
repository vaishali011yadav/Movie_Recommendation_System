#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import ast as ast
import dill as pickle


# In[4]:


movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')


# In[5]:


movies.head(1)


# In[6]:


credits.head(1)


# In[7]:


movies=movies.merge(credits,on='title')


# In[8]:


movies.head(1)


# In[9]:


#genere
#id
#keyword
#title
#overwiew
#cast
#crew
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[10]:


movies.info()


# In[11]:


movies.head()


# In[12]:


movies.isnull().sum()


# In[13]:


movies.dropna(inplace=True)


# In[14]:


movies.duplicated().sum()


# In[15]:


movies.iloc[0].genres


# In[16]:


#'[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
# ['Action','Adventure','FFantasy','SciFi']


# In[17]:


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


# In[18]:


movies['genres'] = movies['genres'].apply(convert)


# In[19]:


movies.head()


# In[20]:


movies['keywords']=movies['keywords'].apply(convert)


# In[21]:


def convert3(obj):
    L = []
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L


# In[22]:


movies['cast']=movies['cast'].apply(convert3)


# 

# In[23]:


movies.head()


# In[24]:


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i ['job']== 'Director':
            L.append(i['name'])
            break
    return L


# In[25]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[26]:


movies.head()


# In[27]:


movies['overview'][0]


# In[28]:


movies['overview']=movies['overview'].apply(lambda x:x.split())


# In[29]:


movies.head()


# In[30]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[31]:


movies.head()


# In[32]:


movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']


# In[33]:


movies.head()


# In[34]:


new_df=movies[['movie_id','title','tags']]


# In[35]:


new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))


# In[36]:


new_df.head()


# In[37]:


new_df['tags']=new_df['tags'].apply(lambda x:x.lower())


# In[38]:


new_df.head()


# In[39]:


import nltk


# In[40]:


from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[41]:


def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[42]:


new_df['tags']= new_df['tags'].apply(stem)


# In[43]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')


# In[44]:


vectors = cv.fit_transform(new_df['tags']).toarray()


# In[45]:


vectors


# In[46]:


cv.get_feature_names()


# In[47]:


from sklearn.metrics.pairwise import cosine_similarity


# In[48]:


similarity=cosine_similarity(vectors)


# In[49]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[50]:


similarity[0]


# In[51]:


def recommend(movie):
    movie_index=new_df[new_df['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)
    return


# In[52]:


recommend('Avatar')


# In[53]:


new_df.iloc[1216].title


# In[54]:


import pickle


# In[55]:


pickle.dump(new_df,open('movies.pkl','wb'))


# In[57]:


new_df['title'].values


# In[60]:


pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))


# In[61]:


pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:




