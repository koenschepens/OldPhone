# Python Houndify SDK


## Features

The Houndify Python SDK allows you to make streaming voice and text queries to the Houndify API from your Python project. The SDK provides two classes - **TextHoundClient** and **StreamingHoundClient** - which are useful for making text and voice queries to the Houndify API. See the *Usage* section below as well as sample scripts in the SDK for more information.


## Install / Build

The SDK relies on another Python module *pySHSpeex* that handles compressing audio into SoundHound's Speex format. To build and install *pySHSpeex* run following commands:

```bash
cd pySHSpeex
sudo python setup.py install
```
*Note: this will install *pySHSpeex* system-wide although it is possible to install it per-user following standard Python module installation procedure.*


## Using the SDK

The Python SDK ships with sample projects that demonstrate how to use various features. Before you use the SDK, you need a valid Client ID and Client Key. You can get these keys from [Houndify.com](Houndify.com) by registering a new client, and enabling domains.

### Sending Audio Queries

You can send streaming audio to the sample program *sample_wave.py*. There are two `.wav` files you can try. You will get back a [JSON Response](https://docs.houndify.com/reference/HoundServer) based on the contents of the audio. 

```bash
./sample_wave.py <CLIENT ID> <CLIENT KEY> test_audio/whattimeisitindenver.wav
```

There is also another sample program *sample_stdin.py* which will take PCM samples from `stdin`. You can use it with arecord/sox to do real-time decoding from a microphone.

```bash
arecord -t raw -c 1 -r 16000 -f S16_LE | ./sample_stdin.py <CLIENT ID> <CLIENT KEY>
```
```bash
rec -p | sox - -c 1 -r 16000 -t s16 -L - | ./sample_stdin.py <CLIENT ID> <CLIENT KEY>
```

### Sending Text Queries

For an example of text client take a look at the sample project *sample_text.py*. It lets you pass in a text query and returns a [JSON Response](https://docs.houndify.com/reference/HoundServer).

```bash
./sample_text.py <CLIENT ID> <CLIENT KEY> '<QUERY>'
```

## Usage 

The main module in the SDK is *houndify.py*, which contains three classes:

* **TextHoundClient**
* **StreamingHoundClient**
* **HoundListener**

### TextHoundClient

This class is used for making text queries to the Houndify API. The constructor expects:

* `clientID`: This is the Client ID of your Houndify app.
* `clientKey`: This is the Client Key of your Houndify app. 
* `userID`: This parameter should be unique for every user that uses your app.
* `requestInfo`: (optional) This should be a dictionary that will make the JSON response more accurate. See [RequestInfo](https://docs.houndify.com/reference/RequestInfo) for supported keys.

```python
import houndify

clientId = "YOUR_CLIENT_ID"
clientKey = "YOUR_CLIENT_KEY"
userId = "test_user"
requestInfo = {
  'ClientID': clientId,
  'UserID': userId,
  'Latitude': 37.388309, 
  'Longitude': -121.973968
}

client = houndify.TextHoundClient(clientId, clientKey, userId, requestInfo)
```

The method that is used for sending a text query is **TextHoundClient.query(query_string)** and it returns a string with [response JSON](https://docs.houndify.com/reference/HoundServer) in it.

```python
reponse = client.query('What is the weather like today?')
```

You can reset [RequestInfo fields](https://docs.houndify.com/reference/RequestInfo) via the **TextHoundClient.setHoundRequestInfo(key, value)** method. For more information, see [The RequestInfo JSON Reference](https://docs.houndify.com/reference/RequestInfo).

```python
client.setHoundRequestInfo('City', 'Santa Clara')
```


### StreamingHoundClient

In order to make send an audio query to the Houndify API you need to initialize a **StreamingHoundClient**. The constructor expects the following arguments:

* `clientID`: This is the Client ID of your Houndify app.
* `clientKey`: This is the Client Key of your Houndify app. 
* `requestInfo`: (optional) This should be a dictionary that will make the JSON response more accurate. See [RequestInfo](https://docs.houndify.com/reference/RequestInfo) for supported keys.
* `sampleRate`: (optional) The sample rate of the audio, either 8000 or 16000 Hz. It will default to 16000 if not supplied.

```python
import houndify

clientId = "YOUR_CLIENT_ID"
clientKey = "YOUR_CLIENT_KEY"
client = houndify.StreamingHoundClient(clientId, clientKey, sampleRate=8000)
```

Additionally you'll need to extend and create **HoundListener**:

```python
class MyListener(houndify.HoundListener):
  def onPartialTranscript(self, transcript):
    print "Partial transcript: " + transcript
  def onFinalResponse(self, response):
    print "Final response: " + str(response)
  def onError(self, err):
    print "ERROR"

# class HoundListener
#   HoundListener is an abstract base class that defines the callbacks
#   that can be received while streaming speech to the server
#
#   def onPartialTranscript(self, transcript)
#     onPartialTranscript is fired when the server has sent a partial transcript
#     in live transcription mode.  'transcript' is a string with the partial transcript
#
#   def onFinalResponse(self, response)
#     onFinalResponse is fired when the server has completed processing the query
#     and has a response.  'response' is the JSON object (as a Python dict) which
#     the server sends back.
#
#   def onTranslatedResponse(self, response)
#     onTranslatedResponse is fired if the server was requested to send the JSON
#     response to an external API.  In that case, this will be fired after
#     onFinalResponse and contain the raw data from the external translation API
#
#   def onError(self, err)
#     onError is fired if there is an error interacting with the server.  It contains
#     the parsed JSON from the server.
```

### Sending Audio Requests: Code Example

Finally, you should start a request with passing an instance of your Listener to *StreamingHoundClient.start(listener)*, pipe the audio through *StreamingHoundClient.fill(samples)* and call *StreamingHoundClient.finish()* when request is done. 

*Note: StreamingHoundClient supports 8/16 kHz 16-bit little-endian PCM samples.*

```python 
class MyListener(houndify.HoundListener):
  def onPartialTranscript(self, transcript):
    print "Partial transcript: " + transcript
  def onFinalResponse(self, response):
    print "Final response: " + str(response)
  def onError(self, err):
    print "ERROR"
    
    
client.start(MyListener())
#samples is the list of 16-bit little-endian PCM samples
client.fill(samples)
client.finish()
```

### Sending Audio Requests: Useful Methods

There are three more useful methods in *StreamingHoundClient* for resetting sample rate, location and request info fields.

```python
client.setSampleRate(8000) #or 16000
client.setLocation(37.388309, -121.973968)
client.setHoundRequestInfo('City', 'Santa Clara')
```