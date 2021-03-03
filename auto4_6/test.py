from auto4_6 import *

time.sleep(0.5)
img = getImage(L_SUPPORT_IMAGE_BOX)
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
cv2.imwrite("initial_IMG/L_support.png", img)
