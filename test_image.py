import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from PIL import Image
import io

img_size = (256, 256)
#model = tf.keras.models.load_model('my_model.keras')
model = tf.keras.models.load_model('my_model.keras')
tf.keras.models.load_model('my_model')

# Function to preprocess the attached image
def preprocess_image_for_model(image_bytes):
    """Preprocess a single image for prediction from image bytes."""
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes))

    # Convert to RGB if the image has an alpha channel (RGBA)
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Resize with padding to match the input shape of the model
    image = tf.image.resize_with_pad(np.array(image), target_height=img_size[0], target_width=img_size[1])

    # Normalize pixel values to [0, 1]
    image = tf.cast(image, tf.float32) / 255.0

    # Add a batch dimension since the model expects batches of images
    return tf.expand_dims(image, axis=0)

def classify_image(image):
    """Classify an image using the trained model."""

    # Make a prediction
    predictions = model.predict(image, verbose = 0)

    # Get the predicted class and confidence
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]

    return predicted_class, confidence

def check_for_raidbots(image):

    # Preprocess the image
    preprocessed_image = preprocess_image_for_model(image)

    # Get the predicted class label and prediction scores
    predicted_class, confidence = classify_image(preprocessed_image)
    if predicted_class == 1 and confidence > 0.8:
        return True
