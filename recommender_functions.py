"""CSC108 A3 recommender starter code."""

from typing import TextIO, List, Dict

from recommender_constants import (MovieDict, Rating, UserRatingDict,
                                   MovieUserDict)
from recommender_constants import (MOVIE_FILE_STR, RATING_FILE_STR,
                                   MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL,
                                   MOVIE_USER_DICT_SMALL)


############## HELPER FUNCTIONS

def get_similarity(user1: Rating, user2: Rating) -> float:
    """Return the a similarity score between user1 and user2 based on their
    movie ratings. The returned similarity score is a number between 0 and 1
    inclusive. The higher the number, the more similar user1 and user2 are.

    For those who are curious, this type of similarity measure is called the
    "cosine similarity".

    >>> r1 = {1: 4.5, 2: 3.0, 3: 1.0}
    >>> r2 = {2: 4.5, 3: 3.5, 4: 1.5, 5: 5.0}
    >>> s1 = get_similarity(r1, r1)
    >>> abs(s1 - 1.0) < 0.0001 # s1 is close to 1.0
    True
    >>> s2 = get_similarity(r1, {6: 4.5})
    >>> abs(s2 - 0.0) < 0.0001 # s2 is close to 0.0
    True
    >>> round(get_similarity(r1, r2), 2)
    0.16
    """
    shared = 0.0
    for m_id in user1:
        if m_id in user2:
            shared += user1[m_id] * user2[m_id]
    norm1 = 0.0
    for m_id in user1:
        norm1 = norm1 + user1[m_id] ** 2
    norm2 = 0.0
    for m_id in user2:
        norm2 = norm2 + user2[m_id] ** 2
    return (shared * shared) / (norm1 * norm2)


############## STUDENT CONSTANTS

MINIMUM_RATE = 3.5


############## STUDENT HELPER FUNCTIONS
def get_can(similar_user_dic: Dict[int, float],
            target_rating: Rating,
            user_ratings: UserRatingDict,
            movie_users: MovieUserDict) -> List[List]:
    """
    get candidate movies.
    """
    movies2 = []
    movies = []
    for user in similar_user_dic:
        for movie in user_ratings[user]:
            if movie not in target_rating and user_ratings[user][movie] >= MINIMUM_RATE:
                if movie not in movies2:
                    movies2.append(movie)
                    movies.append([movie, 0, len(movie_users[movie])])
    return movies


def get_movie_score(similar_user_dic: Dict[int, float],
                    target_rating: Rating,
                    user_ratings: UserRatingDict,
                    movie_users: MovieUserDict) -> List[List]:
    """
    Return a dictionary containing all movies that might be recommanded with there score.
    """
    user_score = {}
    movies = get_can(similar_user_dic, target_rating, user_ratings, movie_users)
    for user in similar_user_dic:
        user_score[user] = 0
        for movie in movies:
            if movie[0] in user_ratings[user] \
                    and user_ratings[user][movie[0]] >= MINIMUM_RATE:
                user_score[user] += 1
    for user in similar_user_dic:
        for movie in movies:
            if movie[0] in user_ratings[user] \
                    and user_ratings[user][movie[0]] >= MINIMUM_RATE:
                score = movie[1]
                score += similar_user_dic[user] / \
                         (user_score[user] * movie[2])
                movie[1] = score
    return movies


def get_rank(num_movies: int, score_list: List, movie_score: Dict[int, List[int]]):
    """
    return movie with correct rank
    """
    movie_list = []
    for score in score_list:
        same_score = []
        for movie in movie_score:
            if score == movie_score[movie][0]:
                same_score.append(movie)
        same_score.sort()
        if len(same_score) + len(movie_list) <= num_movies:
            movie_list.extend(same_score)
        else:
            movie_list.extend(same_score[:(num_movies - len(movie_list))])
    return movie_list


############## STUDENT FUNCTIONS

def read_movies(movie_file: TextIO) -> MovieDict:
    """Return a dictionary containing movie id to (movie name, movie genres)
    in the movie_file.

    >>> movfile = open('movies_tiny.csv')
    >>> movies = read_movies(movfile)
    >>> movfile.close()
    >>> 68735 in movies
    True
    >>> movies[124057]
    ('Kids of the Round Table', [])
    >>> len(movies)
    4
    >>> movies == MOVIE_DICT_SMALL
    True
    """
    dic = {}
    for line in movie_file.readlines()[1:]:
        line = line.strip('\n')
        movie_list = line.split(',')
        id = movie_list[0]
        title = movie_list[1]
        genres = movie_list[4:]
        dic[int(id)] = (title, genres)
    return dic


def read_ratings(rating_file: TextIO) -> UserRatingDict:
    """Return a dictionary containing user id to {movie id: ratings} for the
    collection of user movie ratings in rating_file.

    >>> rating_file = open('ratings_tiny.csv')
    >>> ratings = read_ratings(rating_file)
    >>> rating_file.close()
    >>> len(ratings)
    2
    >>> ratings[1]
    {2968: 1.0, 3671: 3.0}
    >>> ratings[2]
    {10: 4.0, 17: 5.0}
    """
    dic = {}
    for line in rating_file.readlines()[1:]:
        line = line.strip('\n')
        rating_list = line.split(',')
        id = int(rating_list[0])
        movie = int(rating_list[1])
        rate = float(rating_list[2])
        if id in dic:
            new_dic = dic[id]
            new_dic[movie] = rate
            dic[id] = new_dic
        else:
            dic[id] = {movie: rate}
    return dic


def remove_unknown_movies(user_ratings: UserRatingDict,
                          movies: MovieDict) -> None:
    """Modify the user_ratings dictionary so that only movie ids that are in the
    movies dictionary is remaining. Remove any users in user_ratings that have
    no movies rated.

    >>> small_ratings = {1001: {68735: 5.0, 302156: 3.5, 10: 4.5}, 1002: {11: 3.0}}
    >>> remove_unknown_movies(small_ratings, MOVIE_DICT_SMALL)
    >>> len(small_ratings)
    1
    >>> small_ratings[1001]
    {68735: 5.0, 302156: 3.5}
    >>> 1002 in small_ratings
    False
    """
    need_user = []
    for user in user_ratings:
        dic = user_ratings[user]
        need_movie = []
        for movie in dic:
            if movie not in movies:
                need_movie.append(movie)
        for movie in need_movie:
            del dic[movie]
        if user_ratings[user] == {}:
            need_user.append(user)
    for user in need_user:
        del user_ratings[user]


def movies_to_users(user_ratings: UserRatingDict) -> MovieUserDict:
    """Return a dictionary of movie ids to list of users who rated the movie,
    using information from the user_ratings dictionary of users to movie
    ratings dictionaries.

    >>> result = movies_to_users(USER_RATING_DICT_SMALL)
    >>> result == MOVIE_USER_DICT_SMALL
    True
    """
    dic = {}
    for user in user_ratings:
        user_dic = user_ratings[user]
        for movie in user_dic:
            if movie in dic:
                dic[movie].append(user)
            else:
                dic[movie] = [user]
    return dic


def get_users_who_watched(movie_ids: List[int],
                          movie_users: MovieUserDict) -> List[int]:
    """Return the list of user ids in moive_users who watched at least one
    movie in moive_ids.

    >>> get_users_who_watched([293660], MOVIE_USER_DICT_SMALL)
    [2]
    >>> lst = get_users_who_watched([68735, 302156], MOVIE_USER_DICT_SMALL)
    >>> len(lst)
    2
    """
    user_list = []
    for movie in movie_ids:
        if movie in movie_users:
            user_list.extend(movie_users[movie])
    user_list_set = set(user_list)
    user_list = list(user_list_set)
    user_list.sort()
    return user_list


def get_similar_users(target_rating: Rating,
                      user_ratings: UserRatingDict,
                      movie_users: MovieUserDict) -> Dict[int, float]:
    """Return a dictionary of similar user ids to similarity scores between the
    similar user's movie rating in user_ratings dictionary and the
    target_rating. Only return similarites for similar users who has at least
    one rating in movie_users dictionary that appears in target_Ratings.

    >>> sim = get_similar_users({293660: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL)
    >>> len(sim)
    1
    >>> round(sim[2], 2)
    0.86
    """
    movie_list = []
    for key in target_rating:
        movie_list.append(key)
    similar_user = get_users_who_watched(movie_list, movie_users)
    dic = {}
    for user in similar_user:
        dic[user] = get_similarity(target_rating, user_ratings[user])
    return dic


def recommend_movies(target_rating: Rating,
                     movies: MovieDict,
                     user_ratings: UserRatingDict,
                     movie_users: MovieUserDict,
                     num_movies: int) -> List[int]:
    """Return a list of num_movies movie id recommendations for a target user
    with target_rating of previous movies. The recommendations come from movies
    dictionary, and are based on movies that "similar users" data in
    user_ratings / movie_users dictionaries.

    >>> recommend_movies({302156: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [68735]
    >>> recommend_movies({68735: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [302156, 293660]
    """
    similar_user_dic = get_similar_users(target_rating, user_ratings, movie_users)
    movie_score = get_movie_score(similar_user_dic,
                                  target_rating, user_ratings, movie_users)
    movie_list = []
    for key in movie_score:
        movie_list.append((key[1], key[0]))
    new_movie = []
    for tup in movie_list:
        new_movie.append((-tup[0], tup[1]))
    new_movie.sort()
    new_movie = new_movie[:num_movies]
    new_m = []
    for movie in new_movie:
        new_m.append(movie[1])
    return new_m


if __name__ == '__main__':
    """Uncomment to run doctest"""
    import doctest

    doctest.testmod()
