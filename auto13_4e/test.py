from auto13_4e import *

time.sleep(0.5)
img = getImage(COMBAT_END_CLICK_BOX)
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
#cv2.imwrite("initial_IMG/combat_finish.png", img)



