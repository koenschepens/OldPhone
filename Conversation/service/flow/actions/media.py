import flow.state
import flow.initial
import flow.contexts
import flow.actions
import kodi

try:
    import xbmcgui
except:
    pass
import time

import conversation
from actionState import actionState
from spotifyState import spotifyState
from userInput import userInput

class media(actionState):

    def handle(self, result):
        self.Context.log("handle media: " + str(result.Parameters))

    def video_play(self, result):
        if("service_name" in result.Parameters):
            if(result.Parameters["service_name"] == "youtube"):
                self.Context.log("youtube play: " + str(result.Parameters))
            else:
                self.play_movie(result)
        else:
            self.play_movie(result)

    def video_search(self, result):
        self.Context.log("video_search: " + str(result.Parameters))

    def play_movie(self, result):
        params = result.Parameters
        if('title' in params and params['title'] != '$title'):
            q = params['title']
            url = 'plugin://plugin.video.kodipopcorntime/search?query=' + q + ''
        elif('searchQuery' in params and params['searchQuery'] != '$q'):
            q = params['searchQuery']
            url = 'plugin://plugin.video.kodipopcorntime/search?query=' + q + ''
        elif('genre' in params and params['genre'] != '$genre'):
            url = 'plugin://plugin.video.kodipopcorntime/genres/' + params['genre'] + '/1?limit=20'
        else:
            url = "plugin://plugin.video.kodipopcorntime/genres"

        container = self.Context.ActivateWindow(url, window='videos')
       
    def music_play(self, result):
        self.spotify_play(result)

    def temp(self):        
        self.Context.SendAction('PlayMedia', 'plugin://plugin.video.youtube/?path=/root/search&action=play_video&videoid=' + youtubeId )

    def spotify_play(self, result):
        spot = spotifyState(self.Context)
        spot.do_login()
        results = spot.do_search(result)
        for track in results.tracks:
            self.Context.log("link: " + str(track.link))
            self.Context.log("artist: " + str(track.artists[0].name))
            self.Context.log("name: " + str(track.name))
            self.Context.CreateWindow()

        self.Context.SendAction('PlayMedia', 'plugin://plugin.video.youtube/' )
        
        #track_uri = 'spotify:track:6xZtSE6xaBxmRozKA0F6TA'
        
    def music_search(self, result):
        self.Context.log("search music: " + str(result.ParsedJson))
