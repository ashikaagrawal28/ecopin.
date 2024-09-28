import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os
    
cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API_KEY'), 
    api_secret = os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

class CloudinaryFunc:
    def upload_image(image):
        upload_result = cloudinary.uploader.upload(image)
        return {'image_url': upload_result["secure_url"], 'asset_id': upload_result["asset_id"]}