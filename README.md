**Image Magic: Build an Automated Image Resizing Pipeline with Email Alerts using AWS S3, Lambda, SNS & Terraform (Step-by-Step)**

In today’s visually-driven digital world, images make or break user experience. Slow-loading large images hurt SEO, increase bandwidth costs, and frustrate users on mobile devices. Yet manually resizing and optimizing every uploaded image is tedious, error-prone, and doesn’t scale.

**What if every image you upload to S3 is automatically resized, optimized, saved to a separate bucket, and you get an instant email notification — all without lifting a finger?**

That’s exactly the **serverless Image Magic pipeline** we’re building today using **AWS S3, Lambda, SNS, and Terraform**.

This hands-on project is perfect for developers, DevOps engineers, and cloud enthusiasts looking to strengthen their portfolio and land better opportunities.

### The Business Problem
E-commerce stores, content platforms, and marketing teams deal with thousands of images daily. Without automation:
- Websites load slowly
- Storage and transfer costs skyrocket
- Teams waste hours on repetitive resizing tasks
- Inconsistent image quality across devices and platforms

A fully automated, event-driven pipeline solves these issues instantly.

### Why This Solution Stands Out
This architecture delivers:
- **Zero manual intervention** — Upload once, everything else is automatic
- **Real-time email alerts** via SNS
- **Infrastructure as Code (IaC)** with Terraform for version control and reproducibility
- **Serverless efficiency** — Pay only for actual usage
- **Scalable & production-ready** design

It beautifully demonstrates **event-driven architecture**, **serverless computing**, and **IaC skills** — highly valued by recruiters.

### What We’ll Build
- **Source S3 Bucket** — Upload raw images here
- **AWS Lambda Function** (Python + Pillow) — Automatically resizes images (configurable percentage & JPEG quality)
- **Destination S3 Bucket** — Stores optimized resized images
- **SNS Topic** — Sends professional email notifications on successful processing
- Everything provisioned cleanly with **Terraform**

**GitHub Repo**: [https://github.com/mathesh-me/image-resizing-using-s3-lambda-sns](https://github.com/mathesh-me/image-resizing-using-s3-lambda-sns)

---

### Prerequisites
- Active AWS account with admin permissions
- Terraform installed (v1.0+)
- AWS CLI configured (optional but recommended)
- VS Code or any code editor
- Basic Python knowledge

---

### Project Structure
```
.
├── main.tf
└── python/
    └── image-resizing-s3.py
```

---

### Step 1: Terraform Configuration (`main.tf`)

Create `main.tf` with the following complete code:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.74.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"  # Change to your preferred region
}

# Random suffix for unique bucket names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

# Source Bucket
resource "aws_s3_bucket" "source_bucket" {
  bucket = "source-image-bucket-${random_string.suffix.id}"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "Source Image Bucket"
    Environment = "DevOpsLab"
    Owner       = "Mathesh"
  }
}

# Destination Bucket
resource "aws_s3_bucket" "destination_bucket" {
  bucket = "resized-image-bucket-${random_string.suffix.id}"

  tags = {
    Name        = "Resized Image Bucket"
    Environment = "DevOpsLab"
    Owner       = "Mathesh"
  }
}

# SNS Topic
resource "aws_sns_topic" "image_resize_notifications" {
  name = "ImageResizingNotifications"

  tags = {
    Name        = "Image Resize Notifications"
    Environment = "DevOpsLab"
  }
}

# Email Subscription (Confirm after terraform apply)
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.image_resize_notifications.arn
  protocol  = "email"
  endpoint  = "your-email@example.com"  # ← CHANGE THIS
}
```

*(The full `main.tf` including IAM Role, Lambda function, S3 trigger, and permissions is available in the GitHub repo. It uses a public Pillow Lambda Layer for easy deployment.)*

---

### Step 2: Lambda Function Code (`python/image-resizing-s3.py`)

This Python script handles the core logic:

```python
import os
import json
import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
sns = boto3.client('sns')

DESTINATION_BUCKET_NAME = os.environ.get('DESTINATION_BUCKET_NAME')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
RESIZE_PERCENTAGE = float(os.environ.get('RESIZE_PERCENTAGE', '50')) / 100.0
JPEG_QUALITY = int(os.environ.get('JPEG_QUALITY', '75'))

def lambda_handler(event, context):
    # ... (full handler logic processes S3 upload, resizes image, saves to destination, and sends SNS notification)
    # Full code in GitHub repo
    pass
```

Key features:
- Downloads image from source bucket
- Resizes while maintaining aspect ratio
- Optimizes JPEG quality
- Uploads processed image
- Publishes success notification to SNS

---

### Step 3: Deploy the Pipeline

```bash
terraform init
terraform plan
terraform apply
```

After deployment:
1. Confirm the SNS email subscription
2. Upload a `.jpg` image to the **source bucket**
3. Watch the magic: Resized image appears in destination bucket + email arrives

---

### Demo Results
(Insert your screenshots here — highly recommended)

- Source vs Resized image comparison
- S3 buckets showing files
- Lambda execution logs in CloudWatch
- Sample email notification received
- Terraform apply output

---

### Key Takeaways & Best Practices
- **Use tags** everywhere for better governance
- Leverage **Lambda Layers** for dependencies (Pillow in this case)
- Add error handling, dead-letter queues, and retries for production
- Monitor costs with AWS Budgets
- Extend this project: Support multiple resize formats (thumbnail, medium, large), more image types, or add image validation

---

### Conclusion
This automated image resizing pipeline is more than a lab — it’s a **production-grade solution** you can proudly showcase in interviews and on your resume.

It proves your ability to design event-driven, serverless architectures using modern tools.

**Star the repo** if you found this helpful:  
👉 [https://github.com/mathesh-me/image-resizing-using-s3-lambda-sns](https://github.com/mathesh-me/image-resizing-using-s3-lambda-sns)

What would you like to add next? Multiple image sizes? Slack notifications? Let me know in the comments!

**Follow me for more practical AWS, Terraform, and DevOps hands-on guides.**

*Tags: AWS, Terraform, Lambda, S3, SNS, Serverless, DevOps, Cloud Computing, Image Processing, Automation*

---

**Pro Tips for Ranking on Medium:**
- Add 10+ relevant screenshots (before/after, console views, email)
- Use a compelling featured image (create one showing the architecture)
- Publish Tuesday–Thursday morning
- Share on LinkedIn, Twitter/X, and relevant Reddit subs right after publishing

This version is optimized for Medium’s algorithm: strong hook, clear value, actionable code, visuals encouragement, and calls-to-action.

Copy, add your screenshots, and publish! Let me know if you need the complete `main.tf` file cleaned up or an architecture diagram description. Good luck — this should drive solid traffic and profile visibility! 🚀
