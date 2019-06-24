import pandas as pd;
"""
What data objects objects?
  Ngrams, words, communication modality (subjects, objects, etc)
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
      find_coocurrance_patterns, # (aka itemsets, e.g., milk and bread)
      find_sequential_patterns,
      find_structure_patterns # (e.g., graphs, trees)
    )
  )
)(df)
