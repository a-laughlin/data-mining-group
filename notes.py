import pandas as pd;
"""
Project Type
Inference vs predictive?
  Inference
Categoriation vs Regression?
  Categorization

Glossary:
  Choose Document Unit (e.g., paragraph, document, book):
    Precision/Recall tradeoff. In search, small units (e.g., sentences) may miss longer themes. Large ones (e.g. books) dilute results to irrelevance.
  Sentencise (spacy makes this part of dependency parsing, and combines it with a few other things)
  Tokenize

  Remove stop words (optional, for performance, depends on purpose)
    Stop words increase sentence precision, but also increase memory and processing time if they aren't needed
    a, and, the https://nlp.stanford.edu/IR-book/html/htmledition/dropping-common-terms-stop-words-1.html
  POS Tag (assign Part of Speech tags)
  Normalize Equivalencies (i.e., synonyms)
    https://nlp.stanford.edu/IR-book/html/htmledition/normalization-equivalence-classing-of-terms-1.html
  Normalize morphology (reduce inflectional word forms to a common base) via stemming or lemmatization
    Stemming usually chops endings off.  Often removes derivational affixes.  Faster. Returns stems.
    Lemmatization analyzes vocabulary and morphology, normally removing inflectional endings only. More accurate. Returns lemmas.


What data objects objects?
  Ngrams, words, parts of speech tags, communication modality
  # In general, linguists use morphological, syntactic, and semantic clues to determine the category of a word.
  https://www.nltk.org/book/ch05.html#sec-how-to-determine-the-category-of-a-word

Dimensions?
  temporal space(time), physical space, linguistic space, semantic(concept) space, emotional space, thought space, geographical space, physical context space, interpersonal space, communication mode space(modality)
What measured?
- Trend, oscillation, rate of change, cycles, seasons (regular cycles), noise, relationship patterns(i.e. structures)
- 1-n relationships: proximity,similarity,correlation,frequency,intensity(amplitude),variability, rate of change
What thinking?
  Topics, values, beliefs
How Thinking?
  Sentiment (Positive/Negative), optimism/pessimism, personality
What visualized?
  Juxtaposition, extremes, outliers
"""


# pipeline for each format we need: bag of words, ngrams, structure
# models: ngram
# skip-gram: predicting the context given a word
# bow(bag of words) predicting the word given its context
# cbow(continuous bag of words)
  # 2 ways to train cbow models: normalized hierarchical softmax and non-normalized negative sampling. They work differently.
# desired output
# tenses (optimism vs pessimism) (via tokenization) https://www.nltk.org/book/ch05.html
# sentiment

# pipeline
#   splitting to sentences
#   tag parts of speech (pos tagging)
#   count frequency


#
# Categorization

pipe(
  clean_for_tenses,

)
pipe(
  scrape,
  pipe(#ensure_quality
    accuracy,
    completeness,
    consistency,
    interpretability,
    believability,
    timeliness
  ),
  pipe(#cleaning
    pipe(#dimensionality_reduction (cols)
      pca,
      stepwise_selection,
      best_subset,
      remove_irrelevant,
      derive_more_useful_attributes,
      remove_colinearity
    ),
    pipe(#numerosity_reduction (rows)
      replace_with_distributions,
      bin,
      cluster,
      sample
    ),
    pipe(# transformation
      rescale
    ),
    pipe(
      find_coocurrance_patterns, # (aka itemsets, e.g., milk and bread) algorithms: apriori (depends on transactions?)
      find_sequential_patterns,
      find_structure_patterns, # (e.g., graphs, trees)
      generate_association_rules # (dmct 6.2.2)
    )
  )
)(df)
