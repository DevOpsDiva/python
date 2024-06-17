import boto3

def get_eks_clusters_versions(profile_name, region):
    try:
        # Create a boto3 session with the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an EKS client
        eks_client = session.client('eks', region_name=region)

        # List all clusters
        response = eks_client.list_clusters()

        # Initialize a dictionary to store cluster versions
        cluster_versions = {}

        # Iterate through each cluster and get its version
        for cluster_name in response['clusters']:
            try:
                cluster_info = eks_client.describe_cluster(name=cluster_name)
                k8s_version = cluster_info['cluster']['version']
                cluster_versions[cluster_name] = k8s_version
            except eks_client.exceptions.ResourceNotFoundException:
                print(f"Cluster '{cluster_name}' not found or describe access denied.")
            except Exception as e:
                print(f"Error getting version for cluster '{cluster_name}': {e}")

        return cluster_versions

    except boto3.exceptions.Boto3Error as e:
        print(f"Boto3 error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    aws_profile = 'your_aws_profile'
    region = 'your_region'

    cluster_versions = get_eks_clusters_versions(aws_profile, region)

    if cluster_versions:
        print("Kubernetes versions for EKS clusters:")
        for cluster_name, version in cluster_versions.items():
            print(f"Cluster '{cluster_name}': {version}")
    else:
        print(f"Failed to retrieve Kubernetes versions for AWS profile '{aws_profile}'")
