
from PIL import ImageGrab



class Tools_Hack:

	def __init__(self):
		pass
	
	def screen_grabbing(
		self
		, save_screen_grab_to = 'e:\\screen_grab.jpeg'
	):
		ImageGrab.grab().save(save_screen_grab_to, "JPEG")
		pass