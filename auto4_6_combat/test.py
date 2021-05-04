from auto4_6 import *

time.sleep(0.5)
img = getImage(CHAPTER_3_CLICK_BOX)
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
#cv2.imwrite("initial_IMG/_5_6.png", img)
