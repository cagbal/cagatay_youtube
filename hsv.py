import cv2 

# oku  
image = cv2.imread('cagatay.jpg') 

# çevir
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

# maviyi filtrele
blue_hsv_image = cv2.inRange(hsv_image, (100, 50, 50), (140, 255, 255))

# orijinal ve maviyi birleştir
blue_image = cv2.bitwise_and(image, image, mask=blue_hsv_image)

# horizantal olarak birleştir
horizontal_image = cv2.hconcat([image, blue_image])

# göster
cv2.imshow('HSV image', horizontal_image) 
 
cv2.waitKey(0) 

cv2.destroyAllWindows()