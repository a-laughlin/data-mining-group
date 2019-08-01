import json
from utils import arr2d_from_dict_values,csv_from_arr2d,pipe
import pandas as pd
from a_laughlin_fp import write_json_file
index_json_to_dict = lambda :json.load(open('./data/scrape_index.json'))['resolved']
try:
  import en_core_web_sm # for spacy
except:
  print('spacy language module needed')
  print('run $ `python -m spacy download en_core_web_sm` from the command line')

clean_index_dict=pipe(
  # omit non-content post indices, and guest authors
  lambda d:{k:v for k,v in d.items() if 'author' in v and v['author']=='ritholtz'},
)

index_dict_to_post_meta_csv = pipe(
  arr2d_from_dict_values(['year','month','day','author','title','key']),
  lambda arr:([y,m,d,a,t,k.replace("/","_")+".txt"] for y,m,d,a,t,k in arr),# align path with post filenames
  csv_from_arr2d(out_path="./data/post_meta.csv",cols=['year','month','day','author','title','Filename'])
)

post_meta_and_liwc_to_liwc_features_csv = pipe(
  lambda :[
    pd.read_csv('./data/post_meta.csv').set_index("Filename"),
    pd.read_csv('./data/liwc.csv').set_index("Filename")
  ],
  lambda arr:arr[0].join(arr[1]),
  lambda df:df.to_csv('./data/liwc_features.csv')
)



from os import getcwd
def posts_meta_and_post_files_to_posts_csv(): # adapted from ExtractContent.ipynb
    df = pd.read_csv("./data/post_meta.csv")
    postContent = []
    for blogName in df['Filename']:
      with open('../posts/'+blogName) as blogPost:
        text = ''
        for line in blogPost:
            text += line #hmm... this strips newlines, not escapes them.
        postContent.append(json.dumps(text))
    df['Content'] = postContent
    df.to_csv('data/posts.csv')


posts_csv_to_linguistic_features_json = pipe(
  lambda: pd.read_csv('./data/posts.csv'),
  lambda df:documents_to_linguistic_features_dict(df.Filename,df.Content.map(json.loads)),
  write_json_file('./data/linguistic_features.json')
)
def documents_to_linguistic_features_dict(keys,documents):
  import spacy
  nlp = spacy.load("en_core_web_sm")
  ret={}
  word_counts='word_counts'
  for key,content in zip(keys,documents):
    ret[key]={}
    wc=ret[key][word_counts]={}
    doc = nlp(content)
    t=None
    for token in doc:
      if token.text in wc: wc[token.text]+=1;
      elif not token.is_stop and not token.is_punct and not token.is_space: wc[token.text]=1;
      # all tokens that arent stop words, punctuations,or spaces  # nouns = [token.pos_ == "NOUN"]
  return ret;

scrape_index_to_post_meta_csv = pipe(
  index_json_to_dict,
  clean_index_dict,
  index_dict_to_post_meta_csv
)

pipeline = pipe(
  # scrape_index_to_post_meta_csv,
  # post_meta_and_liwc_to_liwc_features_csv,
  # posts_meta_and_post_files_to_posts_csv,
  posts_csv_to_linguistic_features_json
)

if __name__ == '__main__':
  pipeline()
