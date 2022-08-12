# Ref https://medium.com/geekculture/youtube-videos-download-using-python-codes-3b6183825f0b
# from random import shuffle
from pytube import YouTube
import os
import shutil

while True:
    # Option
    print(
        "#############################################################################"
    )
    print(
        "########                                                             ########"
    )
    print(
        "########               Please choose option to download              ########"
    )
    print(
        "########                                                             ########"
    )
    print(
        "########                    Choose a option:                         ########"
    )
    print(
        "########                                                             ########"
    )
    print(
        "########        1) Download single link                              ########"
    )
    print(
        "########        2) Download from file youtube.list                   ########"
    )
    print(
        "########        3) Exit                                              ########"
    )
    print(
        "########                                                             ########"
    )
    print(
        "#############################################################################"
    )
    chosen_element = input("Enter a number from 1 to 3: ")
    if int(chosen_element) == 1:  # Option download mp3 from single url

        while True:
            # url input from user
            link = input(
                "Enter the URL of the video you want to download(or Enter to quite): \n>> "
            )
            if not link:
                break
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            print("Title:", yt.title)
            print("Author:", yt.author)
            print("Published date:", yt.publish_date.strftime("%Y-%m-%d"))
            print("Number of views:", yt.views)
            print("Length of video:", yt.length, "seconds")
            # for e in yt.streams:
            #     print(e)
            # Extract Audio only.
            audioFile = (
                yt.streams.filter(abr="160kbps", progressive=False).first().download()
            )

            # Write to log file to keep track
            with open("youtube.log", "a+", encoding="utf-8") as f:
                f.write("# " + yt.title + "\n")
                f.write(link + "\n")

            # Save to mp3 file
            # base, ext = os.path.splitext(audioFile)
            # audioFileNew = base + ".mp3"
            # shutil.move(audioFile, audioFileNew)
    elif int(chosen_element) == 2:  # Option download mp3 from youtube.list
        with open("youtube.list", "r") as f:
            for link in f:
                # Ignore line with begin #
                if not link.startswith("#"):
                    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
                    print("Title:", yt.title)
                    print("Author:", yt.author)
                    print("Published date:", yt.publish_date.strftime("%Y-%m-%d"))
                    print("Number of views:", yt.views)
                    print("Length of video:", yt.length, "seconds")
                    # for e in yt.streams:
                    #     print(e)
                    # Extract Audio only.
                    audioFile = (
                        yt.streams.filter(abr="160kbps", progressive=False)
                        .first()
                        .download()
                    )
                    # Write to log file to keep track
                    with open("youtube.log", "a+", encoding="utf-8") as wf:
                        wf.write("# " + yt.title + "\n")
                        wf.write(link + "\n")
                    # Save to mp3 file
                    # base, ext = os.path.splitext(audioFile)
                    # audioFileNew = base + ".mp3"
                    # shutil.move(audioFile, audioFileNew)
    elif (
        int(chosen_element) == 3
    ):  # Option 3, we rename all mp3 files and move to yt_mp3 folder
        # Get the current Directory
        parentDir = os.getcwd()

        # Create 'process' folder in current folder
        os.makedirs("process", exist_ok=True)
        # Create 'complete' folder in current folder
        os.makedirs("yt_mp3", exist_ok=True)

        processPath = os.path.join(parentDir, "process")
        completePath = os.path.join(parentDir, "yt_mp3")

        # All mp3 files in 'parentDir'
        allfiles = os.listdir(parentDir)
        mp3Files = [fname for fname in allfiles if fname.endswith(".webm")]

        # Move all mp4 files to 'processPath'
        for f in mp3Files:
            # print(os.path.join(parentDir, f))
            shutil.move(os.path.join(parentDir, f), processPath)

        # Change to 'processFolder' and change name file
        os.chdir(processPath)
        for f in os.listdir():
            fTitle, fExt = os.path.splitext(f)
            fTitle = fTitle.title()
            fExt = fExt.lower()
            newName = "{}{}".format(fTitle, fExt)
            os.rename(f, newName)
            # Move all processed mp4 files to 'completePath'
            # shutil.move(os.path.join(processPath, newName), completePath)
            shutil.copy2(os.path.join(processPath, newName), completePath)
            os.remove(os.path.join(processPath, newName))
        break
    else:
        print("Sorry, the value entered must be a number from 1 to 3, then try again!")
