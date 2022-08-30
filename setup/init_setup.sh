echo '-Setting up initial AWS environment'
echo '-S3 bucket for email app : ' $ATTACHMENT_S3_BUCKET 
echo '-Step Function Arn : ' $EMAIL_PROCESSOR_STATE_MACHINE_ARN

echo ''
echo '-Listing current S3 bucket'
aws s3 ls s3://$ATTACHMENT_S3_BUCKET
echo '- Copying partner configuration file'
aws s3 cp ../config/hiddeninsight-key-9643.json s3://$ATTACHMENT_S3_BUCKET
echo ''
echo '- Setting up config for partner hiddeninsight'
aws s3 cp ./boy4.jpg s3://$ATTACHMENT_S3_BUCKET/hiddeninsight/boy4.jpg
aws s3 cp ./girl1.jpg s3://$ATTACHMENT_S3_BUCKET/hiddeninsight/girl1.jpg
aws s3 cp ./serverless-application-model.pdf s3://$ATTACHMENT_S3_BUCKET/hiddeninsight/serverless-application-model.pdf

echo ''
echo '- Setting up config for test client greenchalk'
export GC_BUCKET=greenchalkps-emails-7654
aws s3 mb s3://$GC_BUCKET
aws s3 cp ./boy4.jpg s3://$GC_BUCKET/gcps/boy4.jpg
aws s3 cp ./girl1.jpg s3://$GC_BUCKET/gcps/girl1.jpg

echo ''
echo '- Setting up config for test client jackfruithouse'
export JH_BUCKET=jackfruithouse-emails-7654
aws s3 mb s3://$JH_BUCKET
aws s3 cp ./boy4.jpg s3://$JH_BUCKET/boy4.jpg
aws s3 cp ./girl1.jpg s3://$JH_BUCKET/girl1.jpg

echo '-Listing S3 bucket'
aws s3 ls s3://$ATTACHMENT_S3_BUCKET
aws s3 ls s3://$ATTACHMENT_S3_BUCKET/hiddeninsight/
echo "-Listing greenchalk bucket"
aws s3 ls s3://$GC_BUCKET/gcps/
echo "-Listing jackfruithouse bucket"
aws s3 ls s3://$JH_BUCKET

