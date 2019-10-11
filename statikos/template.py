from awacs.aws import Action, Allow, PolicyDocument, Principal, Statement
from awacs.s3 import ARN as S3_ARN
from troposphere import GetAtt, Ref, Template
from troposphere.certificatemanager import Certificate
from troposphere.cloudfront import (
    Cookies, CustomErrorResponse, CustomOriginConfig, DefaultCacheBehavior,
    Distribution, DistributionConfig, ForwardedValues, Logging, Origin,
    ViewerCertificate
)
from troposphere.route53 import AliasTarget, RecordSet, RecordSetGroup
from troposphere.s3 import (
    Bucket, BucketPolicy, LoggingConfiguration, WebsiteConfiguration
)


def create_template(parameters: dict) -> Template:
    """
    Create a CloudFormation template.

    Uses troposphere (https://github.com/cloudtools/troposphere) to
    programmatically build an AWS CloudFormation template.

    :rtype: troposphere.Template
    :return: a troposphere template instance
    """
    t = Template()
    t.add_version('2010-09-09')
    t.set_description('Static website generated with Statikos')

    s3_bucket_logs = \
        Bucket(
            'S3BucketLogs',
            DeletionPolicy='Delete',
            AccessControl='LogDeliveryWrite',
            BucketName=f"{parameters['stack_name']}-logs"
        )

    s3_bucket_root = \
        Bucket(
            'S3BucketRoot',
            DeletionPolicy='Delete',
            AccessControl='PublicRead',
            BucketName=f"{parameters['stack_name']}-root",
            LoggingConfiguration=LoggingConfiguration(
                DestinationBucketName=Ref(s3_bucket_logs),
                LogFilePrefix='/cdn',
            ),
            WebsiteConfiguration=WebsiteConfiguration(
                ErrorDocument='404.html',
                IndexDocument='index.html'
            )
        )

    s3_bucket_policy = \
        BucketPolicy(
            'S3BucketPolicy',
            Bucket=Ref(s3_bucket_root),
            PolicyDocument=PolicyDocument(
                Version='2012-10-17',
                Statement=[
                    Statement(
                      Effect=Allow,
                      Action=[Action('s3', 'GetObject')],
                      Principal=Principal('*'),
                      Resource=S3_ARN(f"{parameters['stack_name']}-root/*")
                    )
                ]
            )
        )

    acm_certificate = \
        Certificate(
            'CertificateManagerCertificate',
            DomainName=parameters['domain_name'],
            ValidationMethod='DNS'
        )

    cloudfront_distribution = \
        Distribution(
            'CloudFrontDistribution',
            DistributionConfig=DistributionConfig(
                Aliases=[parameters['domain_name']],
                CustomErrorResponses=[
                    CustomErrorResponse(
                        ErrorCachingMinTTL=60,
                        ErrorCode=404,
                        ResponseCode=404,
                        ResponsePagePath='/404.html'
                    )],
                DefaultCacheBehavior=DefaultCacheBehavior(
                    AllowedMethods=['GET', 'HEAD'],
                    CachedMethods=['GET', 'HEAD'],
                    Compress=True,
                    DefaultTTL=86400,
                    ForwardedValues=ForwardedValues(
                        Cookies=Cookies(Forward='none'),
                        QueryString=True
                    ),
                    MaxTTL=31536000,
                    SmoothStreaming=False,
                    TargetOriginId=f"S3-{parameters['stack_name']}-root",
                    ViewerProtocolPolicy='redirect-to-https',
                ),
                DefaultRootObject='index.html',
                Enabled=True,
                HttpVersion='http2',
                IPV6Enabled=True,
                Logging=Logging(
                  Bucket=GetAtt(s3_bucket_logs, 'DomainName'),
                  IncludeCookies=False,
                  Prefix='cdn/',
                ),
                Origins=[
                    Origin(
                        CustomOriginConfig=CustomOriginConfig(
                            HTTPPort=80,
                            HTTPSPort=443,
                            OriginKeepaliveTimeout=5,
                            OriginProtocolPolicy='https-only',
                            OriginReadTimeout=30,
                            OriginSSLProtocols=[
                                'TLSv1', 'TLSv1.1', 'TLSv1.2'
                            ]
                        ),
                        DomainName=GetAtt(s3_bucket_root, 'DomainName'),
                        Id=f"S3-{parameters['stack_name']}-root",
                    )],
                PriceClass='PriceClass_All',
                ViewerCertificate=ViewerCertificate(
                    AcmCertificateArn=Ref(acm_certificate),
                    MinimumProtocolVersion='TLSv1.1_2016',
                    SslSupportMethod='sni-only'
                )
            )
        )

    route53_record_set_group = \
        RecordSetGroup(
            'Route53RecordSetGroup',
            HostedZoneName=f"{parameters['domain_name']}.",
            RecordSets=[
                RecordSet(
                    Name=parameters['domain_name'],
                    Type='A',
                    AliasTarget=AliasTarget(
                      DNSName=GetAtt(cloudfront_distribution, 'DomainName'),
                      EvaluateTargetHealth=False,
                      HostedZoneId='Z2FDTNDATAQYW2'
                    )
                ),
                RecordSet(
                    Name=f"www.{parameters['domain_name']}",
                    Type='A',
                    AliasTarget=AliasTarget(
                      DNSName=GetAtt(cloudfront_distribution, 'DomainName'),
                      EvaluateTargetHealth=False,
                      HostedZoneId='Z2FDTNDATAQYW2'
                    )
                )
            ]
        )

    t.add_resource(s3_bucket_logs)
    t.add_resource(s3_bucket_root)
    t.add_resource(s3_bucket_policy)
    t.add_resource(acm_certificate)
    t.add_resource(cloudfront_distribution)
    t.add_resource(route53_record_set_group)
    return t
