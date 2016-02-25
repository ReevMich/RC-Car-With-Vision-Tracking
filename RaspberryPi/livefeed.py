from SimpleCV import Camera

# Basic setup for simpleCV to show a live feed

cam = Camera()

while True:
	img = cam.getImage()
	img = img.binarize()
	img.drawText("Hello World")
	img.show()

