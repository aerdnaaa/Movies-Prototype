import os, secrets

def save_picture(form_picture, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/' + path, picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_video(form_video, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(app.root_path, 'static/videos/' + path, video_fn)
    form_video.save(video_path)
    return video_fn