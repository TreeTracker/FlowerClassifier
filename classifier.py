import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('./model/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open('harsh.jpg')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
image_array = np.asarray(image)

# display the resized image
# image.show()

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference
prediction = model.predict(data)
print(prediction)

finalPrediction = {}

strPrediction = str(prediction)
strPrediction = strPrediction.replace('[','')
strPrediction = strPrediction.replace(']','')

Daisy = ""
Dandelion = ""
Rose = ""
Sunflower = ""
Tulip = ""


strLen = len(strPrediction)
count = 0

for x in range(strLen):
    if strPrediction[x] == " " and strPrediction[x+1] != " ":
        print("hellp")
        count += 1
    if count == 0:
        Daisy += strPrediction[x]
    elif count == 1:
        Dandelion += strPrediction[x]
    elif count == 2:
        Rose += strPrediction[x]
    elif count == 3:
        Sunflower += strPrediction[x]
    else:
        Tulip += strPrediction[x]

finalPrediction["Daisy"] = str(round(float(Daisy.strip()),5) * 100 ) + "%"
print(finalPrediction)
finalPrediction["Dandelion"] = str(round(float(Dandelion.strip()),5) * 100) + "%"
print(finalPrediction)
finalPrediction["Rose"] = str(round(float(Rose.strip()),5) * 100) + "%"
print(finalPrediction)
finalPrediction["Sunflower"] = str(round(float(Sunflower.strip()),5) * 100) + "%"
print(finalPrediction)
finalPrediction["Tulip"] = str(round(float(Tulip.strip()),5) * 100) + "%"

print(finalPrediction)