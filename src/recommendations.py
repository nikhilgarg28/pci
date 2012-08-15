from sets import Set
from collections import defaultdict

# Dummy data for testing purposes
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
    'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
    'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
        'The Night Listener': 4.5, 'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
    }

#Returns a set of common features between bags b1 and b2
def get_common_features(b1, b2):
    common_features = Set()
    for feature in b1:
        if feature in b2:
            common_features.add(feature)
    return common_features

#Returns sum of squares of difference on two lists
def eucledian(l1, l2):
    return sum((l1[i] - l2[i])**2 for i in xrange(len(l1)))

#Returns a distance-based similarity measure for bags b1 and b2
def sim_distance(b1, b2):
    # Similarity measure is to be calculated only on common features
    common_features = get_common_features(b1, b2)
    if len(common_features) == 0:
        return 0

    common_feature_vectors = [(b1[f], b2[f]) for f in common_features]
    distance = eucledian(*zip(*common_feature_vectors))
    similarity = 1 / ( 1 + distance)
    return similarity

#Returns the Pearson correlation coefficient for bags b1 and b2
def sim_pearson(b1, b2):
    common_features = get_common_features(b1, b2)
    N = len(common_features)
    if N == 0:
        print 'Yes Im not finding commong features'
        return 0

    common_feature_vectors = [(b1[f], b2[f]) for f in common_features]
    v1, v2 = zip(*common_feature_vectors)

    sum1, sum2 = sum(v1), sum(v2)

    mag1 = sum(x**2 for x in v1)
    mag2 = sum(x**2 for x in v2)

    # Dot product of vectors v1 and v2
    dot = sum (x * y for x, y in zip(v1, v2))

    #Let's calculate numerator and denominator for pearson coefficient
    num = dot - (sum1 * sum2) / N
    from math import sqrt
    den = sqrt((mag1 - (sum1**2) / N) * (mag2 - (sum2**2) / N))
    if den == 0: return 0
    correlation = num / den
    return correlation

# Returns top N bags which are most similar to B from bags in candidates
# B is a bag of features. candidates is a bag of bag of features
def most_similar(B, candidates, num = 5, similarity = sim_pearson):

    scores = [(similarity(B, candidates[c]), c) for c in candidates]

    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[:num]

# Returns upto num number of features that I don't possess yet based on others
def recommend_features(B, others, num = 5, similarity = sim_pearson):

    total_scores = defaultdict(int)
    weighted_scores = defaultdict(int)

    for other in others.values():
        its_similarity = similarity(B, other)
        if its_similarity == 0: continue
        for feature in other:
            if feature not in B:
                total_scores[feature] += its_similarity
                weighted_scores[feature] += its_similarity * other[feature]

    feature_scores = [ (weighted_scores[f] / total, f) for f, total in
            total_scores.items() if total != 0]

    feature_scores.sort()
    feature_scores.reverse()
    return feature_scores[:num]

# Given a bag of bag of features, it returs a new bag where old features become
# bag and bag becomes features
def invert_bag(B):
    inverted_bag = defaultdict(dict)
    for bag in B:
        for feature in B[bag]:
            inverted_bag[feature][bag] = B[bag][feature]
    return dict(inverted_bag)

