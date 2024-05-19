from roboflow import Roboflow
from inference.models.utils import get_roboflow_model
import supervision as sv
import cv2
from shapely.geometry import Point, MultiPoint
import sympy

class Trees:
    def __init__(self, distance, image_path):
        r = distance

        # Import image to get height
        image = cv2.imread(image_path)

        # Get the dimensions of the image
        height, width, channels = image.shape

        # Get roboflow key to grab model
        rf = Roboflow(api_key="dEzAffaLejt9Jep2lqP0")
        project = rf.workspace().project("tree-detection-ekaot")
        model = project.version(1).model

        # Get results based on model with confidence and overlap, low coinfidences give more results
        result = model.predict(image_path, confidence=20, overlap=30).json()

        # Gets the class labels, only one for tree
        labels = [item["class"] for item in result["predictions"]]

        # Use inference to get the detections
        detections = sv.Detections.from_inference(result)

        # Labels and bounding boxes, mainly for debugging
        label_annotator = sv.LabelAnnotator()
        bounding_box_annotator = sv.BoundingBoxAnnotator()

        # Draw labels and bounding boxes
        annotated_image = bounding_box_annotator.annotate(
            scene=image, detections=detections)
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=detections, labels=labels)

        # Get the x and y coordinates of the trees
        # Gets the distance from centroid to base of tree to plot circle
        xs = [item["x"] for item in result["predictions"]]
        ys = [item["y"] for item in result["predictions"]]
        halfheight = [item["height"] / 2 for item in result["predictions"]]

        #Get the radius of ellipse based on distance from base
        radius = []
        for element in range(len(xs)):
            radius.append(r*(((height - (height - ys[element]))/height)**2))

        # Get the tree roots coodrdinates
        treeroots = []
        for element in range(len(xs)):
            treeroots.append((int(xs[element]), int(ys[element] + halfheight[element])))

        # Draw circles and ellipses
        i = 0
        for root in treeroots:
            cv2.circle(annotated_image, root, 5, (0, 255, 0), 2)
            cv2.ellipse(annotated_image, root, (int(radius[i]), int(radius[i])//4), 0, 0, 360, (0, 255, 0), 2)
            i = i+1

        #print(image.shape)
        cv2.circle(annotated_image, (503, 490), 15, (0, 255, 0), 5)
        # Store the annotated image and the tree roots
        self.annotated_image = annotated_image
        self.treeroots = treeroots

        # Store the original image and the ellipses
        self.image = image
        self.radius = radius

    def get_image(self):
        sv.plot_image(self.annotated_image)

    def get_intersection_points(self):
        intersections = []
        x,y = sympy.symbols('x y', real = True)
        #print(self.treeroots)
        realTreeRoots = []
        for root in self.treeroots:
            realTreeRoots.append([root[0], 1280 - root[1]])
        #print(realTreeRoots)
        treeroots_radius = [[realTreeRoots[i], self.radius[i]] for i in range(0, len(realTreeRoots))]
        #print(treeroots_radius)

        tempRoots = treeroots_radius

        for roots in list(treeroots_radius):
            tempRoots.remove(roots)
            for tRoot in tempRoots:
                #print("Root:",roots, " & ","Temp:", tRoot)
                compRadius = [roots[1], tRoot[1]]
                maxRadius = max(compRadius)
                #print("     " + str(roots[0][0]-tRoot[0][0]) + " < " + str(maxRadius//2) + "           " + str(roots[0][1]-tRoot[0][1]) + " < " + str(maxRadius//4))
                if abs(roots[0][0] - tRoot[0][0])<(maxRadius) and abs(roots[0][1] - tRoot[0][1])<(maxRadius // 2):
                    eq1 = sympy.Eq((((x-roots[0][0])**2)/((roots[1])**2))+(((y-roots[0][1])**2)/((roots[1]//4)**2)), 1)
                    eq2 = sympy.Eq((((x-tRoot[0][0])**2)/((tRoot[1])**2))+(((y-tRoot[0][1])**2)/((tRoot[1]//4)**2)), 1)
                    print(eq1, eq2)
                    intersections.append(sympy.solve((eq1, eq2), (x, y)))

        for intersection in intersections:
            for coordinate in intersection:
                x, y = coordinate
                cv2.circle(self.annotated_image, (int(x), 1280 - int(y)), 5, (255, 0, 0), 5)


        sv.plot_image(self.annotated_image)

        return intersections

