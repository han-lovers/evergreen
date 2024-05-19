import cv2
import numpy as np

class fertileLand:
    def __init__(self, image_path, margin):
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color ranges for grass and dirt
        grass_lower = np.array([25, 52, 72], np.uint8)
        grass_upper = np.array([102, 255, 255], np.uint8)

        dirt_lower = np.array([0, 0, 0], np.uint8)
        dirt_upper = np.array([20, 255, 200], np.uint8)

        # Create masks for grass and dirt
        grass_mask = cv2.inRange(hsv, grass_lower, grass_upper)
        dirt_mask = cv2.inRange(hsv, dirt_lower, dirt_upper)

        # Apply erosion and dilation to the grass mask
        kernel = np.ones((5,5),np.uint8)
        grass_mask = cv2.erode(grass_mask, kernel, iterations = 1)
        grass_mask = cv2.dilate(grass_mask, kernel, iterations = 3)

        # Apply erosion and dilation to the dirt mask
        dirt_mask = cv2.erode(dirt_mask, kernel, iterations = 1)
        dirt_mask = cv2.dilate(dirt_mask, kernel, iterations = 3)

        # Find connected components in the grass mask
        num_labels_grass, labels_grass, stats_grass, centroids_grass = cv2.connectedComponentsWithStats(grass_mask, connectivity=8)

        # Find connected components in the dirt mask
        num_labels_dirt, labels_dirt, stats_dirt, centroids_dirt = cv2.connectedComponentsWithStats(dirt_mask, connectivity=8)

        # Create a new mask where only the blobs with an area larger than the threshold are white
        large_grass_mask = np.zeros_like(grass_mask)
        for i in range(1, num_labels_grass):
            if stats_grass[i, cv2.CC_STAT_AREA] > margin:  # Adjust this threshold value as needed
                large_grass_mask[labels_grass == i] = 255

        # Create a new mask where only the blobs with an area larger than the threshold are white
        large_dirt_mask = np.zeros_like(dirt_mask)
        for i in range(1, num_labels_dirt):
            if stats_dirt[i, cv2.CC_STAT_AREA] > margin:  # Adjust this threshold value as needed
                large_dirt_mask[labels_dirt == i] = 255

        # Bitwise-AND mask and original image
        grass_res = cv2.bitwise_and(image, image, mask=large_grass_mask)
        dirt_res = cv2.bitwise_and(image, image, mask=large_dirt_mask)

        self.grass_res = grass_res
        self.dirt_res = dirt_res

    def get_image(self):
        return self.grass_res, self.dirt_res

        # Write the original image and the segmented images to files
        #cv2.imwrite('Original_Image.jpg', image)
        #cv2.imwrite('Grass.jpg', grass_res)
        #cv2.imwrite('Dirt.jpg', dirt_res)