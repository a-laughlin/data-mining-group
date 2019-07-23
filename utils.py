
from funcy import autocurry, ljuxt, rcompose as pipe, merge,lmapcat,lmap,get_in,set_in,identity,flatten,pluck;
set_with = autocurry(lambda path,fn,o:set_in(o, path.split('.') if isinstance(path,str) else path ,fn(o)))
map = autocurry(lmap);
flatmap = autocurry(lmapcat);
# pipe = rcompose
def get(str):
  path=str.split('.')
  return lambda x:get_in(x,path);
spread = lambda fn:lambda arr:fn(*arr)
max_with = lambda fn:lambda arr:max(arr,key=fn)
min_with = lambda fn:lambda arr:min(arr,key=fn)
juxt = spread(ljuxt)

def arr2d_from_dict_values(cols=[]):
  def inner(idx_dict):
    return ([v[c] for c in cols] for k,v in idx_dict.items())
  return inner;

import csv

def csv_from_arr2d(out_path="output.csv",cols=[]):
  def inner(arr2d):
    w = csv.writer(open(out_path, "w"),quoting=csv.QUOTE_MINIMAL)
    w.writerow(cols)
    for row in arr2d: w.writerow(row);
  return inner;
