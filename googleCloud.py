
from google.cloud import storage
from datetime import datetime




def upload_files():
        
    # Setting credentials using the downloaded JSON file
    client = storage.Client.from_service_account_json(json_credentials_path='C:/Flask/IntegrationProject/sreemana-sffs-287bd39b3a2a.json')
        
    # Creating bucket object
    bucket = client.get_bucket('sreemana-sffs')
        
    # Name of the object to be stored in the bucket
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y-%H:%M:%S")
    print(dt_string)
    cloud_filename='FIRE_ALERT-'+dt_string+'.txt'
    
    object_name_in_gcs_bucket = bucket.blob(cloud_filename)
        
    # Name of the object in local file system
        
    object_name_in_gcs_bucket.upload_from_filename('alert.txt')
    return