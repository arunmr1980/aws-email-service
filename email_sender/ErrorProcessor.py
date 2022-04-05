import RegExUtil as regexutil

def get_to_be_suppressed_list(err_response):
    print("Printing error")
    print(err_response)
    print("Printing code")
    print(err_response['Error']['Code'])
    if (err_response['Error']['Code'] == "MessageRejected"):
        return regexutil.get_email_ids(err_response['Error']['Message'])
