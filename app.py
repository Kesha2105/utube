# from flask import Flask, render_template, request
# from pytube import YouTube

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         link = request.form['youtube_link']
        
#         try:
#             download_video(link)
#             return render_template('index.html', message="Download completed successfully!")
#         except Exception as e:
#             return render_template('index.html', error="An error occurred: {}".format(str(e)))
#     return render_template('index.html')

# def download_video(link):
#     youtube_object = YouTube(link)
#     video_stream = youtube_object.streams.get_highest_resolution()
#     video_stream.download()
    
# if __name__ == '__main__':
#     app.run(debug=True)
import os
from flask import Flask, render_template, request, send_file
from pytube import YouTube
from moviepy.editor import AudioFileClip

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form['youtube_link']
        
        try:
            # Download video
            video_file_path = download_video(link)

            # Convert video to audio
            audio_file_path = convert_video_to_audio(video_file_path)

            # Clean up - delete the downloaded video file
            # os.remove(video_file_path)

            if os.path.exists(audio_file_path) and os.path.exists(video_file_path):
                return render_template('index.html', message="Conversion completed successfully!", audio_file_path=audio_file_path, video_file_path=video_file_path)       
        except Exception as e:
            return render_template('index.html', error="An error occurred: {}".format(str(e)))
    return render_template('index.html')

def download_video(link):
    youtube_object = YouTube(link)
    video_stream = youtube_object.streams.get_highest_resolution()
    video_file_path = video_stream.download()
    return video_file_path

def convert_video_to_audio(video_file_path):
    # Generate audio file path
    audio_file_path = video_file_path[:-4] + '.mp3'  # Replace extension with .mp3

    # Convert video to audio using moviepy
    video_clip = AudioFileClip(video_file_path)
    video_clip.write_audiofile(audio_file_path)

    # Close the video clip
    video_clip.close()

    return audio_file_path
@app.route('/play_video')
def play_video():
    video_file_path = request.args.get('video_file_path')
    
    if video_file_path:
        return send_file(video_file_path, mimetype='video/mp4')
    else:
        return "Video file not found."

@app.route('/play_audio')
def play_audio():
    audio_file_path = request.args.get('audio_file_path')
    if audio_file_path:
        return send_file(audio_file_path, mimetype='audio/mp3')
    else:
        return "Audio file not found."

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=8080)
