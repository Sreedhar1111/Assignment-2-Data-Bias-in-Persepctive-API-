#!/usr/bin/env python
# coding: utf-8

# To find data bias, I compared user inputted scoring on messages with Perspective API (a google software that can score input based on toxicity). 

# In[202]:


import os
import numpy as np
import pandas as pd
import time
import json
from googleapiclient.discovery import build
fullCSV = pd.read_csv(r'/Users/sreedhar/Downloads/labeled_and_scored_comments.csv')


# This was the function that we got to help us call Perspective API to compare the results betweeen user input and what Perspective API thinks.

# In[203]:


def get_toxicity_score(comment):
    
  API_KEY = 'AIzaSyBP1tyWgWXbMdhp67I1CWnCGGfxSlpqepo' 
    
  client = build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
  )

  analyze_request = {
  'comment': { 'text': comment },
  'requestedAttributes': {'TOXICITY': {}}
  }
    
  response = client.comments().analyze(body=analyze_request).execute()
  toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    
  return toxicity_score


# I decided to call all of the things into perspective API and then see the things that have the biggest differences. ( I had to split it inot 2 because I got timed out.

# In[204]:


Perspective_List = []
#print(fullCSV.score[1695], fullCSV.score[693], fullCSV.score[5163], fullCSV.score[1825])


# In[205]:


for comment in fullCSV.comment_text:
    score = get_toxicity_score(comment)
    Perspective_List.append(score)
    print(score)
    time.sleep(1)


# In[ ]:


print(len(Perspective_List))


# In[ ]:


print(len(fullCSV.comment_text))


# In[ ]:



for comment in fullCSV.comment_text[4597:]:
    score = get_toxicity_score(comment)
    Perspective_List.append(score)
    print(score)
    time.sleep(1)


# In[ ]:


print(len(Perspective_List))
DifferenceList = []


# This is when I found the differences between each of the scoring systems.

# In[ ]:


for i in range(0, len(Perspective_List)):
    DifferenceList.append(fullCSV.score[i] - Perspective_List[i])


# In[ ]:


print(DifferenceList)


# In[ ]:


max_value = max(DifferenceList)
min_value = min(DifferenceList)
max_index = DifferenceList.index(max_value)
min_index = DifferenceList.index(min_value)
print(max_index, min_index)


# In[ ]:


print(fullCSV.comment_text[max_index], fullCSV.comment_text[min_index])


# In[200]:


comments = []
wordsWithGay = []

for word in fullCSV.comment_text:
    comments.append(word)

for word in comments:
    if 'gay' in word:
        holder = comments.index(word)
        wordsWithGay.append(holder)
print(wordsWithGay)


# In[201]:


differencesInWordsWithGay = []
for num in wordsWithGay:
    differencesInWordsWithGay.append(DifferenceList[num])
print(differencesInWordsWithGay)


# I found that the biggest differences are between words that contain the word "gay" in them, which I found to be interesting as the connotation of gay can be widely different in context. 

# In[ ]:





# In[ ]:





# In[ ]:




