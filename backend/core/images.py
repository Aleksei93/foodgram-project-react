import hashlib


def upload_to(instance, filename):
    class_folder = instance.__class__.__name__.lower()

    hash_object = hashlib.sha1(filename.encode())
    fname = hash_object.hexdigest()
    extension = filename.split('.')[-1]

    f1 = fname[:2]
    f2 = fname[2:4]
    f3 = fname[4:]

    return f'{class_folder}/{f1}/{f2}/{f3}.{extension}'
