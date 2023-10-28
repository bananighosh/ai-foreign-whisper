import pathlib
from pytube import Playlist
from pytube.exceptions import AgeRestrictedError

# make a directory to download videos into
destination_folder = "./videos"
pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)

# playlist URL -- 60 min youTube channel
URL = "https://youtube.com/playlist?list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&si=23f9dxT9gEKR3AB7"
p = Playlist(URL)

# download the first 10 videos that are not age restricted
# don't require logging in)

n_downloads = 0
for video in p.videos:
    if n_downloads >= 10:
        break

    try:
        print(f"Downloading: {video.title}")
        video.streams.first().download(destination_folder)
    except AgeRestrictedError:
        print("Age restricted, skipping ...")
    else:
        print(f"Successfuly downloaded {video.title}")
        n_downloads += 1

        # download captions
        try:
            if "captions" not in video.vid_info:
                video.bypass_age_gate()
                # this fixes missing caption bug
                # https://github.com/pytube/pytube/issues/1674
            assert "captions" in video.vid_info

            # write english captions
            captions = video.captions["a.en"]
            with open(f"{video.title}_captions.txt", "w") as f:
                f.write(captions.generate_srt_captions())
                # this part is buggy, see issue here
                # https://github.com/pytube/pytube/issues/1085
        except KeyError:
            print(f"error download captions for {video.title}")
        else:
            print(f"successfully download captions for {video.title}")
