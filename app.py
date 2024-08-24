from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

FORMATS = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global FORMATS
    selected_format_url = None
    video_url = request.form.get('video_url')

    if request.method == 'POST':
        if video_url:
            if 'format_id' in request.form:
                # Handle format selection and get the URL from the formats list
                format_id = request.form.get('format_id')
                
                selected_format = next((fmt for fmt in FORMATS if fmt['format_id'] == format_id), None)
                if selected_format:
                    selected_format_url = selected_format.get('url')
            else:
                # Fetch available formats
                FORMATS = get_available_formats(video_url)

    return render_template('index.html', formats=FORMATS, selected_format_url=selected_format_url)

def get_available_formats(video_url):
    global FORMATS
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'listformats': True,
        'cookiesfrombrowser': ('safari',)
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        FORMATS = info.get('formats', [])
        return FORMATS

if __name__ == '__main__':
    app.run(debug=True)
