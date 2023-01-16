## Architecture Diagram

![Email Service - Architecture drawio](https://user-images.githubusercontent.com/19325896/184797164-f3b3f09d-eb74-4808-a36f-eee3089671b9.png)

## Processing functions

Processing is done by the following

### QueueReaderFunction

This is a lambda function that reads message from the queue, validates the request and invoke the Step function

### EmailProcessingStateMachine

This is a step function that orchestrated the following lambda functions.

- EmailSenderFunction: This function sends the email using SES. If attachments are present it also loads the attachments.

- ResponseProcessorFunction: This function processes the response. It checks if there are failures. If the failures are recoverable, it posts the requests back to the queue. If the failures are permanent, it moves the request to DLQ. It also tracks the number of retry attempts. Requests with more retries than the configured threshold are moved to DLQ as well.

## How to use the application?

Once the application is deployed in AWS, client use it by posting a request to SNS

### Request Format
```
{
	"client_ref_transaction_key": "message-9876-987",
	"transaction_key": "nhy6-o98u-9987",
	"from": "arun_mr549e@protonmail.com", 
	"partner_key": "hiddeninsight-key-9643",
	"client_key": "mountlitera-key-1238",
	"to_addresses": [
		{
			"email": "merry.arun@gmail.com", 
		}, 
		{
			"email": "arun.mr@hiddeninsight.in", 
		}
	], 
	"title": "Email Service Test [SNS Trigger] HI", 
	"body_html": "<p>Blah Blah</p>", 
	"body_text": "Blah Blah",
	"attachments":[
    		{
      			"name": "bob.jpg",
      			"file_key": "boy4.jpg"
    		},
    		{
      			"name": "susie.jpg",
      			"file_key": "girl1.jpg"
    		}
  	]

}
```

#### Field Definitions

- client_ref_transaction_key: Any reference key client choose to send. This can be used later for retrieving logs or status. Optional
- transaction_key: A unique transaction key client may want to send to identify this request. Optional
- from: From address of the email. Required
- partner_key: Partner key for the partner configuration. Required
- client_key: Client key in case partner support multiple clients. Optional
- title: Subject line of the email. Required
- body_html: Email content as html. Either of body_html or body_text is required
- body_text: Email content as text. Either of body_html or body_text is required
- to_addresses: List of to addresses
- attachments: List of attachments

#### To address fields
- email: Email address of the recipient. Required

#### Attachment fields
- name: Name of the attachment file
- file_key: File key of the file in S3 

## Installation and setup

1. Install docker(https://docs.docker.com/engine/install/ubuntu/)
2. Install SAM (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
3. Build the application
> sam build --use-container
4. Deploy the application in AWS. AWS user needs all required permissions.
> sam deploy --guided

## Running tests

Run unit tests, integration tests and end to end tests. This will make sure that everything is setup correctly.

1. Setup env variables. Update env_setup.sh with correct values.
> cd setup

> vi env_setup.sh

> . env_setup.sh
2. Update the partner config file. It is in config folder named as [partner_key].json. Update partner and client S3 bucket names if they have changed. 
3. Setup the initial AWS env to run tests
> ./init_setup.sh
4. Run local tests. Note that some tests may need deployed application. If using SES in sandbox make sure that test email addresses are verified. NOTE: The environment variables in the shell you run tests from must be correct. It may be necessary to run env_setup.sh from the shell for a fresh setup.
> python3 -m unittest discover
5. Run end to end tests. Test emails and emails with attachments.
> python3 -m tests.e2e.sns_test
6. Load test with same code as step 8. Increase the mail count. Make sure that step functions type is 'EXPRESS' not 'STANDARD'. Running load test with step function type as 'STANDARD' will escalate billing.

## Features

- Sends emails in a batch
- Support multiple attachments
- Sends emails even if one or more emails fail. It does not block the entire batch

## Service Limits

- Maximum number of attachments - 5
- Maximum attachment size - 5 MB

## Configurations

Configuration is done for partners and clients of each partner. Multiple partners may be configured.

### Partner level configuration

There is a configuration file at the root level of application S3 bucket for each partner.
Here is a sample
```
{
	"name": "HiddenInsight",
	"partner_key":"hiddeninsight-key-9643",
	"s3_bucket_name": "email-app-attachmentsbucket-ehxhya82j2tm",
	"s3_folder_name": "hiddeninsight",
	"clients": [
		{
			"name": "mountlitera",
			"client_key": "mountlitera-key-1238",
			"s3_folder_name": "mountlitera"
		},
		{
			"name": "greenchalk-public-school",
			"client_key": "greenchalkps-key-8528",
			"s3_folder_name": "gcps",
			"s3_bucket_name": "greenchalkps-emails-uw8271"
		},
		{
			"name": "Jackfruit House",
			"client_key": "jackfruithouse-key-4261",
			"s3_bucket_name": "jackfruithouse-emails-uw8271"
		}

	]
}

```
Note that clients of the partner are also configured in this file. Client configuration is optional. 

's3_folder_name' is the folder where the attachments files are saved. There are multiple ways of configuring it.
- When client configuration is not available, it is saved in the folder mentioned in root level.
- Client may keep the attachments in a folder inside the root bucket. See 'mountlitera' configuration in example.
- Client may keep the attachments in a folder inside specified client s3 bucket. See 'greenchalk-public-school' configuration in example.
- Client may keep the attachments inside specified client s3 bucket at its root level. See 'Jackfruit House' configuration in example.


## Quick reference

Build application
> sam build --use-container

Test locally
> sam local invoke EmailSenderFunction --event events/event.json

Unit Test
> python3 -m unittest discover

Deploy to AWS
> sam deploy

Delete infra Stack
> aws cloudformation delete-stack --stack-name email-sender-app


# email-service

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- email_sender - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code.
- template.yaml - A template that defines the application's AWS resources.


## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
email-service$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
email-service$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
email-service$ sam local start-api
email-service$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
email-service$ sam logs -n HelloWorldFunction --stack-name email-service --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
email-service$ pip install -r tests/requirements.txt --user
# unit test
email-service$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
email-service$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name email-service
```

## useful commands

List cloudformation stacks
>aws cloudformation list-stacks

Describe the stack
>aws cloudformation describe-stack-resources --stack-name <STACK_NAME> --query 'StackResources[].{ResourceType:ResourceType,LogicalResourceId:LogicalResourceId, PhysicalResourceId:PhysicalResourceId}' --output table


## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
