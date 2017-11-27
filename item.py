#A class for storing movie information

class movie_item(object):   
    def __init__(self, title,  popularity,  poster_path, episode, original_language, original_title,  overview,  release_date):
        self.title = title
        self.popularity = popularity
        self.poster_path = poster_path
        self.episode = episode
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.release_date = release_date
        
    def GetTitle(self):
        return self.title
    def GetPopularity(self):
        return self.popularity
    def GetPosterPath(self):
        return self.poster_path
    def GetEpisode(self):
        return self.episode
    def GetOriginalLanguage(self):
        return self.original_language
    def GetOriginalTitle(self):
        return self.original_title
    def GetOverview(self):
        return self.overview
    def GetReleaseDate(self):
        return self.release_date
    
    def PrintItem(self):
        print('Title: ' + self.title)
        print('Popularity: ' + str(self.popularity))
        
        if self.poster_path is not None:
            print('Poster Path: ' + str(self.poster_path))
            
        print('Episode #: ' + str(self.episode))
        print('Original Language: ' + str(self.original_language))
        print('Original Title: ' + str(self.original_title))
        print('Overview: ' + str(self.overview))
        print('Release Date: ' + str(self.release_date))
        
#A class for storing anime movie information
        
class anime_item(object):
    def __init__(self, title,  average_rating,  poster_path, episode, japanese_title,  overview,  release_date):
        self.title = title
        self.average_rating = average_rating
        self.poster_path = poster_path
        self.episode = episode
        self.japanese_title = japanese_title
        self.overview = overview
        self.release_date = release_date
        
    def GetTitle(self):
        return self.title
    def GetAverageRating(self):
        return self.average_rating
    def GetPosterPath(self):
        return self.poster_path
    def GetEpisode(self):
        return self.episode
    def GetJapaneseTitle(self):
        return self.japanese_title
    def GetOverview(self):
        return self.overview
    def GetReleaseDate(self):
        return self.release_date
    
    def PrintItem(self):
        print('Title: ' + str(self.title))
        print('Average Rating: ' + str(self.average_rating))
        
        if self.poster_path is not None:
            print('Poster Path: ' + str(self.poster_path))
            
        print('Episode #: ' + str(self.episode))
        print('Japanese Title: ' + str(self.japanese_title))
        print('Overview: ' + str(self.overview))
        print('Release Date: ' + str(self.release_date))