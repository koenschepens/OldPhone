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
from userInputRequired import userInputRequired

class media(actionState):

    def handle(self, result):
        self.Context.log("handle media: " + str(result.Parameters))

    def video_play(self, result):
        self.Context.log("video_play: " + str(result))

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
        
        """if(container.NumItems == 1):
            self.Context.show_notification("Error", "No things found for " + result.ResolvedQuery)
            self.Context.State = initial.Initial(self.Context)
        elif(container.NumItems == 2):
            item = container.getItemByPosition(1)
            item.play()
            self.Context.State = initial.Initial(self.Context)
        else:
            self.Context.State = userInputRequired(self.Context)
            userChoice = self.Context.State.handle(result)
            item = None
            while(item is None):
                item = container.getItemByLabel(userChoice)
            item.play()
            self.Context.State = initial.Initial(self.Context)"""
       
    def music_play(self, result):
        self.Context.log("music_play: " + str(result))
        searchParameters = []
        if('artist' in result.Parameters):
            # So we know the artist, use youtube for now
            searchParameters.append(result.Parameters['artist'])
        if('q' in result.Parameters):
            searchParameters.append(result.Parameters['q'])
            
        youtubeId = self.Context.search_youtube((' '.join(searchParameters)).strip())
        self.Context.SendAction('PlayMedia', 'plugin://plugin.video.youtube/?path=/root/search&action=play_video&videoid=' + youtubeId )

    def music_search(self, result):
        self.Context.log("search music: " + str(result.ParsedJson))
