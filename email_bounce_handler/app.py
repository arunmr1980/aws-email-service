
import ESLogger as eslogger


""" SNS Trigger """
def lambda_handler(event, context):

    eslogger.info("event aka message :-")
    eslogger.info(event)
