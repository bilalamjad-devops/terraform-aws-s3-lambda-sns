# image-resizing-s3.py
import os
import json
import boto3
from PIL import Image
from io import BytesIO

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Get configuration from environment variables set by Terraform
DESTINATION_BUCKET_NAME = os.environ.get('DESTINATION_BUCKET_NAME')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

# Get resize percentage and JPEG quality from environment variables
# Defaults are provided if environment variables are not set
RESIZE_PERCENTAGE_STR = os.environ.get('RESIZE_PERCENTAGE', '50') # Default to 50%
JPEG_QUALITY_STR = os.environ.get('JPEG_QUALITY', '75') # Default to 75 quality

# Validate and convert RESIZE_PERCENTAGE
try:
    RESIZE_PERCENTAGE = float(RESIZE_PERCENTAGE_STR) / 100.0
    if not (0 < RESIZE_PERCENTAGE <= 1):
        raise ValueError("RESIZE_PERCENTAGE must be between 1 and 100.")
except ValueError as e:
    print(f"Warning: Invalid RESIZE_PERCENTAGE environment variable. Using default 50%. Error: {e}")
    RESIZE_PERCENTAGE = 0.5 # Default to 50% if conversion fails or out of range

# Validate and convert JPEG_QUALITY
try:
    JPEG_QUALITY = int(JPEG_QUALITY_STR)
    if not (0 <= JPEG_QUALITY <= 100):
        raise ValueError("JPEG_QUALITY must be between 0 and 100.")
except ValueError as e:
    print(f"Warning: Invalid JPEG_QUALITY environment variable. Using default 75. Error: {e}")
    JPEG_QUALITY = 75 # Default to 75 if conversion fails or out of range

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    # Crucial check: Ensure environment variables are set before proceeding
    if not DESTINATION_BUCKET_NAME or not SNS_TOPIC_ARN:
        print("Error: DESTINATION_BUCKET_NAME or SNS_TOPIC_ARN environment variable is not set.")
        raise ValueError("Configuration error: Missing environment variables. Please check your Lambda environment settings set by Terraform.")

    # Process each record in the S3 event (Lambda can receive multiple events in one invocation)
    if 'Records' in event:
        for record in event['Records']:
            handle_s3_record(record)
    else:
        # Handle single S3 event (for older Lambda versions or specific S3 event types)
        handle_s3_record(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Image processing complete for all records!')
    }

def handle_s3_record(record):
    # Validate the S3 event record structure
    if 's3' not in record or 'bucket' not in record['s3'] or 'name' not in record['s3']['bucket'] \
       or 'object' not in record['s3'] or 'key' not in record['s3']['object']:
        print(f"Error: Invalid S3 event record structure. Skipping record: {json.dumps(record)}")
        return # Skip this record and continue if part of a batch

    # Extract relevant information from the S3 event
    source_bucket = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']
    file_size = record['s3']['object'].get('size', 'N/A')

    print(f"Processing file: {object_key} from bucket: {source_bucket} (Size: {file_size} bytes)")

    try:
        # 1. Download the original image from the source S3 bucket
        print(f"Downloading {object_key} from {source_bucket}...")
        response = s3.get_object(Bucket=source_bucket, Key=object_key)
        content_type = response['ContentType']
        image_data = response['Body'].read()
        print(f"Downloaded {object_key}. Content-Type: {content_type}")

        # 2. Resize and compress the image using PIL (Pillow)
        original_width, original_height = 0, 0 # Initialize dimensions for logging
        resized_width, resized_height = 0, 0   # Initialize dimensions for logging

        try:
            image_buffer, original_width, original_height, resized_width, resized_height = \
                resize_and_compress_image(image_data, RESIZE_PERCENTAGE, JPEG_QUALITY)
            print(f"Image '{object_key}' resized from {original_width}x{original_height} to {resized_width}x{resized_height} (Quality: {JPEG_QUALITY}).")
        except Exception as img_err:
            print(f"Error during image processing (resize/compress) for {object_key}: {img_err}")
            raise # Re-raise to trigger error notification and mark Lambda invocation as failed

        # 3. Upload the processed image to the destination S3 bucket
        # Prepend 'resized/' to the key to put it in a subfolder
        destination_key = f"resized/{object_key}"
        print(f"Uploading resized image to {DESTINATION_BUCKET_NAME}/{destination_key}...")
        s3.put_object(
            Bucket=DESTINATION_BUCKET_NAME,
            Key=destination_key,
            Body=image_buffer,
            ContentType=content_type # Keep original content type
        )
        print(f"Successfully uploaded resized image to {DESTINATION_BUCKET_NAME}/{destination_key}.")

        # 4. Send a success notification to the SNS topic
        # Using the simplified message format you requested
        message = f"Image {object_key} has been resized and uploaded to {DESTINATION_BUCKET_NAME}."
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Image Resizing Success Notification"
        )
        print(f"SNS Success notification published for {object_key}. Message: '{message}'")

        print(f"Successfully processed {object_key}")

    except Exception as e:
        error_message = f"Failed to process {object_key} from {source_bucket}. Error: {e}"
        print(f"An unexpected error occurred: {error_message}")

        # Send an error notification to the SNS topic
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps({ # Keeping error message as JSON for more detail
                "statusCode": 500,
                "error": error_message,
                "key": object_key,
                "source_bucket": source_bucket
            }, indent=2),
            Subject="Image Resizing Error Notification"
        )
        print(f"SNS Error notification published for {object_key}. Error: {e}")
        # Re-raise the exception for Lambda to record it as a failed invocation
        raise e

def resize_and_compress_image(image_data, resize_percentage, quality):
    """
    Opens an image, resizes it by a given percentage, compresses it (if JPEG),
    and returns the processed image as bytes along with dimensions.
    """
    image = Image.open(BytesIO(image_data))
    original_width, original_height = image.size

    # Calculate new dimensions, ensuring they are at least 1x1
    new_width = max(1, int(original_width * resize_percentage))
    new_height = max(1, int(original_height * resize_percentage))

    # Perform resizing using LANCZOS filter for high-quality downsampling
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Prepare an in-memory buffer to save the image
    image_io = BytesIO()

    # Determine format for saving. If original is not JPEG, and we want to apply quality,
    # it's often converted to JPEG. PNG compression quality behaves differently.
    save_format = resized_image.format if resized_image.format else 'JPEG'
    if save_format == 'JPEG':
        resized_image.save(image_io, format=save_format, quality=quality)
    else:
        # For non-JPEG formats (like PNG), quality argument might be ignored or mean something else.
        # So we pass it conditionally, or handle specific formats if needed.
        try:
            resized_image.save(image_io, format=save_format, quality=quality)
        except TypeError: # quality arg not supported for this format
             resized_image.save(image_io, format=save_format)

    image_io.seek(0) # Rewind the buffer to the beginning

    return image_io.getvalue(), original_width, original_height, new_width, new_height 
