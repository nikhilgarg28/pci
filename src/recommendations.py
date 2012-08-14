from sets import Set

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
    return sum([(l1[i] - l2[i])**2 for i in xrange(len(l1))])

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

print sim_distance(critics['Lisa Rose'], critics['Toby'])
