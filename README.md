To run test on your computer you should have installed all required software and please edit 
desired capabilities depending on your device.

Currently test checks if splashscreen appears (via cv2.compareHist) and then 
looking for Mannor Matters logo on loading screen (via cv2.matchTemplate).
