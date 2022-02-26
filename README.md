# Toggle Live Track

Toggle live track is a small script that I use in combination with [executor](https://github.com/raujonas/executor) gnome shell extension to display the current time entry in the top bar. That let me be more time aware whenever I'm working with the computer.

An image is worth a thousand words (except if you take a photo of a text with more than 1000 words, of course)
![img](0415dc7df96de4f19273b8db773ed3d0.png)

If you find it interesting and want to give a go, just:
1. Install a virtual environment (pyenv does not work): `python3 venv venv/`
2. Install requirements `pip install -r requirements.txt`
3. Clone `env_sample` and fill it with your toggl details.
4. Go to executor extension and add the path to your script:
`cd path/to/live_track && source venv/bin/activate && source .env && python live_track.py`

Depending the global installation on your computer you might not even need a virtual environment (just `requests` is needed out from the standard library)

That easy!
