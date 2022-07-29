from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib', 'requests_html', 
    'beautifulsoup4', 
    'youtube_dl',
    'pathlib',
    'pandas'
]

setup(
    name = "SpotifyToYoutubeMP3",
    version = "1.0",
    description = 'spotify to youtube to mp3',
    author = 'ryan',
    author_email = 'ryantsui786@gmail.com',
    keywords = 'web flask',
    packages = find_packages(),
    include_package_data = True,
    install_requires = requires
)