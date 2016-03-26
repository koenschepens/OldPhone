from Conversation.service.flow.states.statebase import StateBase

try:
    import xbmcgui
except:
    pass

class media(StateBase):

    def handle(self, result):
        self.context.log("handle media: " + str(result.Parameters))

    def video_play(self, result):
        if("service_name" in result.Parameters):
            if(result.Parameters["service_name"] == "youtube"):
                self.context.log("youtube play: " + str(result.Parameters))
            else:
                self.context.play_movie(result)
        else:
            self.context.play_movie(result)

    def video_search(self, result):
        self.context.log("video_search: " + str(result.Parameters))
       
    def music_play(self, result):
        self.spotify_play(result)

    def spotify_play(self, result):
        try:
            from spotifyState import spotifyState

            spot = spotifyState(self.context)
            spot.do_login()
            results = spot.do_search(result)
            for track in results.tracks:
                self.context.log("link: " + str(track.link))
                self.context.log("artist: " + str(track.artists[0].name))
                self.context.log("name: " + str(track.name))
                self.context.CreateWindow()

            self.context.SendAction('PlayMedia', 'plugin://plugin.video.youtube/' )

            #track_uri = 'spotify:track:6xZtSE6xaBxmRozKA0F6TA'
        except:
            self.context.show_notification("Spotify not installed")
        
    def music_search(self, result):
        self.context.log("search music: " + str(result.ParsedJson))
