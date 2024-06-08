import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2_client = boto3.client('ec2')
    
    # Retrieve all EBS volumes in the region
    try:
        response = ec2_client.describe_volumes()
        volumes = response['Volumes']
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error describing volumes: {str(e)}'
        }
    
    # Iterate through each volume and encrypt if not already encrypted
    for volume in volumes:
        volume_id = volume['VolumeId']
        encrypted = volume.get('Encrypted', False)
        if not encrypted:
            try:
                response = ec2_client.modify_volume(
                    VolumeId=volume_id,
                    Encrypted=True
                )
                print(f'Volume {volume_id} encrypted successfully')
            except Exception as e:
                print(f'Error encrypting volume {volume_id}: {str(e)}')
    
    return {
        'statusCode': 200,
        'body': 'Operation complete'
    }
