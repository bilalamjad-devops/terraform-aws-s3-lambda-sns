



Steps:
1. terraform apply
2. See Results
- Buckets
- Lambda
- SNS

3. Test

- Upload image
- image uploaded to resized bucket
- cloudwatch logs
- sns notification

4. terraform destroy



### step 1: terraform apply

plesae change:
- region
- email
- The Lambda layer ARN (ap-south-1:770693421928:layer:Klayers-p39-pillow:1) is for ap-south-1 and Python 3.9. If you change the region, you'll need to find the correct ARN for that region (e.g., from Klayers).

<img width="1600" height="900" alt="s3 - a " src="https://github.com/user-attachments/assets/4b7492a7-11ee-461e-8c87-45b8a48dc8fd" />

<img width="1600" height="900" alt="s3 - b" src="https://github.com/user-attachments/assets/0a2beeb1-0407-4906-9b38-9821c7d6b751" />

<img width="1600" height="900" alt="s3 - c" src="https://github.com/user-attachments/assets/5bf632c7-6bfd-418d-be5a-803973cc8412" />

<img width="1600" height="900" alt="s3 - d" src="https://github.com/user-attachments/assets/99e958cf-93a7-419b-b480-6d99fb721736" />

<img width="1600" height="900" alt="s3 - g " src="https://github.com/user-attachments/assets/a6203907-ead8-4ea8-89e9-da533abf85db" />



### 2. See Results

i) 2 Buckets (source and resized)


<img width="1600" height="900" alt="s3 - 1 " src="https://github.com/user-attachments/assets/f89ca183-e08e-4e08-bd11-94bb20ab4b1d" />

<img width="1600" height="900" alt="s3 - 2" src="https://github.com/user-attachments/assets/19ac178b-48ae-44ed-9348-a17385939262" />

<img width="1600" height="900" alt="s3 - 3" src="https://github.com/user-attachments/assets/3dae0690-d7ad-4b25-be33-a06cf2500204" />

ii) Lambda


<img width="1600" height="900" alt="s3 - 4" src="https://github.com/user-attachments/assets/f2606739-74ba-4b76-9aea-928064e8f71c" />

<img width="1600" height="900" alt="s3 - 6" src="https://github.com/user-attachments/assets/27ff6132-7eb0-45db-9fab-b58304161a7f" />

<img width="1600" height="900" alt="s3 - 7" src="https://github.com/user-attachments/assets/eccf810b-a370-48ff-84c2-b30753763fda" />

<img width="1600" height="900" alt="s3 - 8" src="https://github.com/user-attachments/assets/494f78ff-82af-4c47-a882-9b14b8667d09" />

<img width="1600" height="900" alt="s3 - 9" src="https://github.com/user-attachments/assets/94c3e356-e267-45ac-b467-99fd911a1690" />

iii) SNS



<img width="1600" height="900" alt="s3 - 10" src="https://github.com/user-attachments/assets/b609b7eb-4b95-41f5-857f-8d0efc3d9d7e" />

<img width="1600" height="900" alt="s3 - 11 - blur " src="https://github.com/user-attachments/assets/e2090ac5-f21e-4897-892a-13cab084051d" />

<img width="1600" height="900" alt="s3 - 11" src="https://github.com/user-attachments/assets/79a129f4-0ee8-460e-89b1-7feba9322452" />

<img width="1600" height="900" alt="s3 - 12" src="https://github.com/user-attachments/assets/fb431e6f-9bef-4b56-a68c-7c545c9b82b0" />

<img width="1600" height="900" alt="s3 - 13" src="https://github.com/user-attachments/assets/ac304b20-2713-460f-8d8a-05e718fd2cb3" />

<img width="1600" height="900" alt="s3 - 14 - blur " src="https://github.com/user-attachments/assets/fc93edf8-0bd5-4a8b-807a-da93b2fc211d" />

<img width="1600" height="900" alt="s3 - 14" src="https://github.com/user-attachments/assets/b1bbe9b4-fcaf-443e-9a77-44d2dac319d7" />

---

### 3. Test

- upload image: 

<img width="1600" height="900" alt="s3 - 15" src="https://github.com/user-attachments/assets/19eac6b2-0a82-4010-b077-5ecb51c26979" />

<img width="1600" height="900" alt="s3 - 16" src="https://github.com/user-attachments/assets/5481fc23-8dc5-4daa-a90c-229060db3283" />

<img width="1600" height="900" alt="s3 - 17" src="https://github.com/user-attachments/assets/e4c16b56-3de7-4b29-afe1-587c98b542e9" />

<img width="1600" height="900" alt="s3 - 18" src="https://github.com/user-attachments/assets/05004339-a248-439a-a558-29d63a00c0ab" />

<img width="1600" height="900" alt="s3 - 19" src="https://github.com/user-attachments/assets/e28c917b-133f-47aa-abd4-e3002c0627c3" />


- image uploaded to resized bucket

<img width="1600" height="900" alt="s3 - 20" src="https://github.com/user-attachments/assets/24cc2759-0cf4-475a-81fd-fdc814d821ce" />

<img width="1600" height="900" alt="s3 - 21" src="https://github.com/user-attachments/assets/3c216e11-24f8-474a-bf6e-ab18af3d327d" />

<img width="1600" height="900" alt="s3 - 22" src="https://github.com/user-attachments/assets/3d064cf1-5016-4d99-921b-ee2ef9113648" />

<img width="1600" height="900" alt="s3 - 23" src="https://github.com/user-attachments/assets/a1932e81-76aa-4133-8a1e-e851ac5f28be" />

- cloudwatch logs


<img width="1600" height="900" alt="s3 - 24" src="https://github.com/user-attachments/assets/beb86cc0-f25e-4832-818a-a1b75c19d7ef" />

<img width="1600" height="900" alt="s3 - 25" src="https://github.com/user-attachments/assets/27239319-484e-40a1-8eef-7a8426308f43" />

<img width="1600" height="900" alt="s3 - 26" src="https://github.com/user-attachments/assets/ad5e92da-8e33-4a11-8cb2-5f0cb64b05ec" />

<img width="1600" height="900" alt="s3 - 27 - blur " src="https://github.com/user-attachments/assets/97502153-6490-4e2c-87a3-27e8198e3a71" />

<img width="1600" height="900" alt="s3 - 27 - Copy" src="https://github.com/user-attachments/assets/59378622-36f3-4d06-8242-d96141309fce" />

<img width="1600" height="900" alt="s3 - 27" src="https://github.com/user-attachments/assets/32e10925-9b28-47a6-81ad-62bc11602874" />

### terraform destroy

<img width="1600" height="900" alt="s3 - 28" src="https://github.com/user-attachments/assets/83638ae9-2465-4050-93e7-53f04e179267" />

<img width="1600" height="900" alt="s3 - 29" src="https://github.com/user-attachments/assets/df3508c1-4e25-41cf-8eb3-9e1a97271f5e" />

<img width="1600" height="900" alt="s3 - 33" src="https://github.com/user-attachments/assets/342fcfd5-596a-4d46-b5cf-58a35562b826" />



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
