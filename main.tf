# main.tf

# --- Terraform Configuration ---
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.74.0" # Lock to a specific version for consistency
    }
  }
}

# --- AWS Provider Configuration ---
provider "aws" {
  region     = "ap-south-1"
}

# --------------------------------------------------------------------------------------------------
# RESOURCES
# Defines all the AWS resources for the image resizing system.
# --------------------------------------------------------------------------------------------------

# Generates a random string to append to bucket names for uniqueness
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

# --- S3 Buckets ---
resource "aws_s3_bucket" "source_bucket" {
  bucket = "source-image-bucket-${random_string.suffix.id}" # Hardcoded prefix + random suffix

  # Recommended: Enable versioning on source bucket for safety
  versioning {
    enabled = true
  }

  tags = {
    Name        = "Source Image Bucket"
    Environment = "DevOpsLab"
  }
}

resource "aws_s3_bucket" "destination_bucket" {
  bucket = "resized-image-bucket-${random_string.suffix.id}" # Hardcoded prefix + random suffix

  tags = {
    Name        = "Resized Image Bucket"
    Environment = "DevOpsLab"
  }
}

# --- SNS Topic and Subscription ---
resource "aws_sns_topic" "image_resize_notifications" {
  name = "ImageResizingNotifications" # Hardcoded topic name

  tags = {
    Name        = "Image Resize Notifications"
    Environment = "DevOpsLab"
  }
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.image_resize_notifications.arn
  protocol  = "email"
  endpoint  = "your-email@example.com" # <--- 👈 IMPORTANT: CHANGE THIS TO YOUR ACTUAL EMAIL ADDRESS

  # IMPORTANT: After `terraform apply`, you will receive an email.
  # You MUST click the confirmation link in that email for the subscription to become active.
}

# --- IAM Role and Policy for Lambda ---
resource "aws_iam_role" "lambda_exec_role" {
  name = "ImageResizerLambda-ExecRole" # Hardcoded role name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Name        = "ImageResizerLambda-ExecRole"
    Environment = "DevOpsLab"
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name = "ImageResizerLambda-Policy" # Hardcoded policy name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.source_bucket.arn}/*"
      },
      {
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl", # Needed if your Lambda code sets ACLs (e.g., public-read)
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.destination_bucket.arn}/*"
      },
      {
        Action = [
          "sns:Publish",
        ]
        Effect   = "Allow"
        Resource = aws_sns_topic.image_resize_notifications.arn
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:ap-south-1:*:*" # Uses provider's region directly
      }
    ]
  })

  tags = {
    Name        = "ImageResizerLambda-Policy"
    Environment = "DevOpsLab"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# --- Lambda Function ---
# Zip the Python code for deployment
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/python/image-resizing-s3.py" # Assumes Python file is in 'src' directory
  output_path = "${path.module}/python/image-resizing-s3.zip"
}

resource "aws_lambda_function" "image_resizer_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "ImageResizerLambda" # Hardcoded function name
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "image-resizing-s3.lambda_handler" # Corresponds to your python file and handler function name
  runtime          = "python3.9" # Ensure this matches the Klayers version. Klayers-p39-pillow is for python3.9

  # Using a public Klayers layer for Pillow
  # IMPORTANT: Verify the ARN for your chosen region and Python runtime!
  # The ARN below is for `ap-south-1` and `python3.9`.
  # You can find ARNs for other regions/runtimes at: https://www.lambdalayers.com/
  layers = ["arn:aws:lambda:ap-south-1:770693421928:layer:Klayers-p39-pillow:1"] # Uses provider's region directly

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 60  # Maximum execution time in seconds (adjust if image processing is slow)
  memory_size      = 256 # Memory in MB (adjust as needed for larger images)

  environment {
    variables = {
      DESTINATION_BUCKET_NAME = aws_s3_bucket.destination_bucket.bucket
      SNS_TOPIC_ARN           = aws_sns_topic.image_resize_notifications.arn
      RESIZE_PERCENTAGE       = "50" # Example: Resize to 50% of original size. Adjust this value (e.g., "75" for 75%)
      JPEG_QUALITY            = "75" # Example: JPEG compression quality (0-100)
    }
  }

  tags = {
    Name        = "ImageResizerLambda"
    Environment = "DevOpsLab"
  }
}

# --- S3 Trigger for Lambda ---
# Permission for S3 to invoke Lambda
resource "aws_lambda_permission" "allow_s3_invoke_lambda" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_resizer_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source_bucket.arn
}

# S3 bucket notification configuration to trigger the Lambda
resource "aws_s3_bucket_notification" "s3_trigger" {
  bucket = aws_s3_bucket.source_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.image_resizer_lambda.arn
    events              = ["s3:ObjectCreated:*"] # Trigger on any object creation
    filter_suffix       = ".jpg" # Only trigger for .jpg files (you can add .png, .jpeg etc.)
  }

  # Ensure the Lambda permission is created before the notification
  depends_on = [aws_lambda_permission.allow_s3_invoke_lambda]
} 
