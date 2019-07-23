import json
from utils import arr2d_from_dict_values,csv_from_arr2d,pipe
import pandas as pd

index_json_to_dict = lambda :json.load(open('./data/scrape_index.json'))['resolved'],

clean_index_dict=pipe(
  # omit non-content post indices, and guest authors
  lambda d:{k:v for k,v in d.items() if 'author' in v and v['author']=='ritholtz'},
)

index_dict_to_post_meta_csv = pipe(
  arr2d_from_dict_values(['year','month','day','author','title','key']),
  lambda arr:([y,m,d,a,t,k.replace("/","_")+".txt"] for y,m,d,a,t,k in arr),# align path with post filenames
  csv_from_arr2d(out_path="./data/post_meta.csv",cols=['year','month','day','author','title','Filename']),
)

merge_post_meta_csv_w_liwc_csv = pipe(
  lambda :[
    pd.read_csv('./data/post_meta.csv').set_index("Filename"),
    pd.read_csv('./data/liwc.csv').set_index("Filename")
  ],
  lambda arr:arr[0].join(arr[1]),
)

if __name__ == 'main':
  pipe(
    index_json_to_dict,
    clean_index_dict,
    index_dict_to_post_meta_csv,
    merge_post_meta_csv_w_liwc_csv,
    lambda df:df.to_csv('./data/data.csv')
  )()
