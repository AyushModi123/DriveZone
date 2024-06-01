import firebase_admin
from firebase_admin import credentials, storage
from abc import ABC, abstractmethod
import os

cred = credentials.Certificate(os.environ.get("FIREBASE_PRIVATE_KEY_PATH"))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'project-cemphris.appspot.com'
})

class UploadImage(ABC):
    @abstractmethod
    def upload_image(image_file, directory=None):
        pass

class FirebaseUploadImage(UploadImage):
    @staticmethod
    def upload_image(image_file, directory=None):
        bucket = storage.bucket()
        blob = bucket.blob(f"{directory}/{image_file.name}")
        blob.upload_from_file(image_file)    
        blob.make_public()
        image_url = blob.public_url
        return image_url


