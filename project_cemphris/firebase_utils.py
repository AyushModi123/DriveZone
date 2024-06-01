import firebase_admin
from firebase_admin import credentials, storage
from abc import ABC, abstractmethod

cred = credentials.Certificate(r"C:\Users\ayush\Downloads\project-cemphris-firebase-adminsdk-f3oi6-cc4dec7871.json")
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


