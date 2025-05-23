from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties
from cartography.models.core.nodes import CartographyNodeSchema
from cartography.models.core.relationships import CartographyRelProperties
from cartography.models.core.relationships import CartographyRelSchema
from cartography.models.core.relationships import LinkDirection
from cartography.models.core.relationships import make_target_node_matcher
from cartography.models.core.relationships import OtherRelationships
from cartography.models.core.relationships import TargetNodeMatcher


@dataclass(frozen=True)
class EC2NetworkInterfaceInstanceNodeProperties(CartographyNodeProperties):
    """
    Selection of properties of a network interface as known by an EC2 instance
    """

    # arn: PropertyRef = PropertyRef('Arn', extra_index=True) TODO use arn; issue #1024
    id: PropertyRef = PropertyRef("NetworkInterfaceId")
    status: PropertyRef = PropertyRef("Status")
    mac_address: PropertyRef = PropertyRef("MacAddress", extra_index=True)
    description: PropertyRef = PropertyRef("Description")
    private_dns_name: PropertyRef = PropertyRef("PrivateDnsName", extra_index=True)
    private_ip_address: PropertyRef = PropertyRef("PrivateIpAddress", extra_index=True)
    region: PropertyRef = PropertyRef("Region", set_in_kwargs=True)
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class EC2NetworkInterfaceToAWSAccountRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class EC2NetworkInterfaceToAWSAccountRel(CartographyRelSchema):
    target_node_label: str = "AWSAccount"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {"id": PropertyRef("AWS_ID", set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.INWARD
    rel_label: str = "RESOURCE"
    properties: EC2NetworkInterfaceToAWSAccountRelProperties = (
        EC2NetworkInterfaceToAWSAccountRelProperties()
    )


@dataclass(frozen=True)
class EC2NetworkInterfaceToEC2InstanceRelRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class EC2NetworkInterfaceToEC2InstanceRel(CartographyRelSchema):
    target_node_label: str = "EC2Instance"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {"id": PropertyRef("InstanceId")},
    )
    direction: LinkDirection = LinkDirection.INWARD
    rel_label: str = "NETWORK_INTERFACE"
    properties: EC2NetworkInterfaceToEC2InstanceRelRelProperties = (
        EC2NetworkInterfaceToEC2InstanceRelRelProperties()
    )


@dataclass(frozen=True)
class EC2NetworkInterfaceToEC2SubnetRelRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class EC2NetworkInterfaceToEC2SubnetRel(CartographyRelSchema):
    target_node_label: str = "EC2Subnet"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {"id": PropertyRef("SubnetId")},
    )
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "PART_OF_SUBNET"
    properties: EC2NetworkInterfaceToEC2SubnetRelRelProperties = (
        EC2NetworkInterfaceToEC2SubnetRelRelProperties()
    )


@dataclass(frozen=True)
class EC2NetworkInterfaceToEC2SecurityGroupRelRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class EC2NetworkInterfaceToEC2SecurityGroupRel(CartographyRelSchema):
    target_node_label: str = "EC2SecurityGroup"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {"id": PropertyRef("GroupId")},
    )
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "MEMBER_OF_EC2_SECURITY_GROUP"
    properties: EC2NetworkInterfaceToEC2SecurityGroupRelRelProperties = (
        EC2NetworkInterfaceToEC2SecurityGroupRelRelProperties()
    )


@dataclass(frozen=True)
class EC2NetworkInterfaceInstanceSchema(CartographyNodeSchema):
    """
    Network interface as known by an EC2 instance
    """

    label: str = "NetworkInterface"
    properties: EC2NetworkInterfaceInstanceNodeProperties = (
        EC2NetworkInterfaceInstanceNodeProperties()
    )
    sub_resource_relationship: EC2NetworkInterfaceToAWSAccountRel = (
        EC2NetworkInterfaceToAWSAccountRel()
    )
    other_relationships: OtherRelationships = OtherRelationships(
        [
            EC2NetworkInterfaceToEC2InstanceRel(),
            EC2NetworkInterfaceToEC2SubnetRel(),
            EC2NetworkInterfaceToEC2SecurityGroupRel(),
        ],
    )
