import jetson_inference
import jetson_utils

net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson_utils.gstCamera(1280, 720, "/dev/video1")
display = jetson.utils.glDisplay()



while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network: {:0f} FPD+S".format(net.GetNetworkFPS()))

	for detection in detections:
		print(net.GetClassDesc(detection.ClassID))
