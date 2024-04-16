def razorpay_client_credentials(studio):
    if studio in ["NDA","SD","IPM","GGN"]:
        razorpay_key_id = 'rzp_live_mxqGmvv7wvDwCM'
        razorpay_key_secret = '5Y7eDdJE819LCsBIiiZzgavQ'

    else:
        razorpay_key_id = 'rzp_live_mxqGmvv7wvDwCM'
        razorpay_key_secret = '5Y7eDdJE819LCsBIiiZzgavQ'
    dict = {"id": razorpay_key_id, "secret": razorpay_key_secret}
    print(dict)
    return dict

key = razorpay_client_credentials("ED")['id']
print(key)


