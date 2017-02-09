# The Missing Peace
## Project Overview
Conflict has been extensively studied, giving way to numerous theories behind its causes. With a background in conflict resolution, I wanted to see how machine learning techniques would perform in trying to predict conflict.
For this project, I specifically focused in the MENA region, in the post-World War II era and I examined exclusively intra-state conflict. That is, conflict that happens within one nation’s borders.

## The Data
The data that I used came from a variety of sources and the objective with this data collection was to capture a given country’s political, economic and social situation.

The data, although rich in what it captured, had many instances of missing values. After taking a closer look at these instances of missing data, it was observed that data was missing was correlated with conflict. As such, missing values actually had significance to them, which meant it wouldn’t be ideal to drop them or impute them in any way, as they offered part of the picture of the reality of conflict.

## The Model

With this restriction in terms of data availability, I needed to find a model that could handle missing values. For this reason, I decided to work with Decision Trees,  and by extension Random Forest and Boosting Classifier models.

## The Baseline Model

In order to establish a benchmark or baseline model, I looked into the training set and, by country, calculated the proportion of conflict in the available years of data. If a given country had more than 50% of conflict in the reported instances, the prediction for that country would be that every following year would be a conflict year. If the proportion was less than 50%, the baseline predicted no conflict for the years to follow.

I chose the F1 score as the metric to measure my models against, because it offers a good balance between precision and recall. My baseline model gave me an F1-score of 39%

My first set of models did not perform well. I was a bit too cautious with my train-test set separation to the point where my model could only see the factors affecting any given year in a specific country, without being able to ‘learn’ with time. The F1 score only improved to 45% in the first set of models, so I knew time was a bigger concern than I had first anticipated.

## The Importance of Time
Conflict cannot be looked at in isolation.  In order to correct my model, I decided to more actively incorporate the element of time, by:
a.	lagging values and
b.	including the deltas for the indicators chosen

## The Results 
The best performing model was a random forest with an F1-score of 85%

The results are better than the baseline, which indicates that the chosen indicators had an effect in the overall result of the model.

The features that most contributed to the model most were: conflict the previous year, polity score, political terror scale and unemployment.
