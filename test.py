mpesa_response = {
    'Body': {
        'stkCallback': {
            'MerchantRequestID': '81b9-4f93-88c9-42e42ccd826128287', 'CheckoutRequestID': 'ws_CO_16042026204315633720247234', 'ResultCode': 0, 'ResultDesc': 'The service request is processed successfully.', 'CallbackMetadata': {'Item': [{'Name': 'Amount', 'Value': 1}, {'Name': 'MpesaReceiptNumber', 'Value': 'UDG8E14V6L'}, {'Name': 'Balance'}, {'Name': 'TransactionDate', 'Value': 20260416204323}, {'Name': 'PhoneNumber', 'Value': 254720247234}]}}}}

print(mpesa_response)