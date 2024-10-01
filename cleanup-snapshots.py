from operator import itemgetter

import boto3

ec2_client = boto3.client('ec2', region_name='us-east-2')

snapshots = ec2_client.describe_snapshots

volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['prod']
            }
        ]
    )
for volumes in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {

            'Name': 'volume-id',
            'Values': [volumes['VolumeId']]
            }
        ]
)

sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

for snap in sorted_by_date[2:]:
    response = ec2_client.delete_snapshot(
        SnapshotId=snap['SnapshotId']
    )
    print(response)



