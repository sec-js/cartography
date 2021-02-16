from . import dynamodb
from . import ec2
from . import ecr
from . import eks
from . import elasticsearch
from . import iam
from . import lambda_function
from . import organizations
from . import permission_relationships
from . import rds
from . import redshift
from . import resourcegroupstaggingapi
from . import route53
from . import s3

from .ec2.auto_scaling_groups import sync_ec2_auto_scaling_groups
from .ec2.instances import sync_ec2_instances
from .ec2.key_pairs import sync_ec2_key_pairs
from .ec2.load_balancers import sync_load_balancers
from .ec2.load_balancer_v2s import sync_load_balancer_v2s
from .ec2.network_interfaces import sync_network_interfaces
from .ec2.security_groups import sync_ec2_security_groupinfo
from .ec2.subnets import sync_subnets
from .ec2.tgw import sync_transit_gateways
from .ec2.vpc import sync_vpc
from .ec2.vpc_peering import sync_vpc_peering


RESOURCE_FUNCTIONS = {
    'iam': iam.sync,
    's3': s3.sync,
    'dynamodb': dynamodb.sync,
    'ec2:autoscalinggroup': sync_ec2_auto_scaling_groups,
    'ec2:instance': sync_ec2_instances,
    'ec2:keypair': sync_ec2_key_pairs,
    # TODO - find a way to allow this in here without running EC2 twice in _sync_one_account().
    # 'ec2': ec2.sync,
    'ec2:load_balancer': sync_load_balancers,
    'ec2:load_balancer_v2': sync_load_balancer_v2s,
    'ec2:network_interface': sync_network_interfaces,
    'ec2:security_group': sync_ec2_security_groupinfo,
    'ec2:subnet': sync_subnets,
    'ec2:tgw': sync_transit_gateways,
    'ec2:vpc': sync_vpc,
    'ec2:vpc_peering': sync_vpc_peering,
    'ecr': ecr.sync,
    'eks': eks.sync,
    'lambda_function': lambda_function.sync,
    'rds': rds.sync,
    'redshift': redshift.sync,
    'route53': route53.sync,
    'elasticsearch': elasticsearch.sync,
    'permission_relationships': permission_relationships.sync,
    'resourcegroupstaggingapi': resourcegroupstaggingapi.sync,
}
