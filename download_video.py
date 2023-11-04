import pathlib
from pytube import Playlist
from pytube.exceptions import AgeRestrictedError

# make a directory to download videos into
destination_folder = "./videos"
captions_folder = "./captions"

pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)
pathlib.Path(captions_folder).mkdir(parents=True, exist_ok=True)

download_captions_as_xml = True  # set to False for string format

# playlist URL -- 60 min youTube channel
URL = "https://youtube.com/playlist?list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&si=23f9dxT9gEKR3AB7"
p = Playlist(URL)

# download the first 10 videos that are not age restricted
# don't require logging in
n_downloads = 0
for video in p.videos:
    if n_downloads >= 10:
        break

    try:
        print(f"Downloading: {video.title} ...", end=" ")
        (video.streams.filter(progressive=True, file_extension='mp4')
         .order_by('resolution').desc().first().download(destination_folder))
    except AgeRestrictedError:
        print("Failed! Age restricted, skipping")
    else:
        print("Success!", end=" ")
        n_downloads += 1

        # download captions
        print("Downloading captions ...", end=" ")
        try:
            if "captions" not in video.vid_info:
                # this fixes missing caption bug
                # https://github.com/pytube/pytube/issues/1674
                video.bypass_age_gate()
            assert "captions" in video.vid_info

            # write english captions to file as xml or str
            captions = video.captions["a.en"]
            if download_captions_as_xml:
                with open(f"{pathlib.Path(captions_folder)/video.title}.xml", "w") as f:
                    f.write(captions.xml_captions)
            else:
                with open(f"{pathlib.Path(captions_folder)/video.title}.txt", "w") as f:
                    f.write(captions.generate_srt_captions())
        except Exception as e:
            print("Failed!")
            raise
        else:
            print("Success!")
