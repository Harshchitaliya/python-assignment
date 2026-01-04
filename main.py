from load_dataset import DatasetLoader
from user_interface_module import MusicApp


def main():
    try:
        loader = DatasetLoader("data.csv")
        artist_music = loader.load_data()

        app = MusicApp(artist_music)
        app.run()

    except Exception as e:
        print("Error starting application:", e)


if __name__ == "__main__":
    main()
