#!/usr/bin/python

from flask import request, redirect, Flask, render_template
from ccavutil import encrypt, decrypt
from ccavResponseHandler import res
from string import Template

app = Flask('ccavRequestHandler')

'''
Please put in the 32 bit alphanumeric key and Access Code in quotes provided by CCAvenues.
'''
accessCode = 'AVKR14KI19BL44RKLB'
workingKey = '868E43E034DB2953A9E18EC401CA3268'


@app.route('/')
def webprint():
    return render_template('dataFrom.htm')


@app.route('/ccavResponseHandler', methods=['GET', 'POST'])
def ccavResponseHandler():
    plainText = res(request.form['encResp'])
    return plainText


@app.route('/ccavRequestHandler', methods=['GET', 'POST'])
def login():
    p_merchant_id = request.form['merchant_id']
    p_order_id = request.form['order_id']
    p_currency = request.form['currency']
    p_amount = request.form['amount']
    p_redirect_url = request.form['redirect_url']
    p_cancel_url = request.form['cancel_url']

    merchant_data = 'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + p_redirect_url + '&' + 'cancel_url=' + p_cancel_url + '&'

    encryption = encrypt(merchant_data, workingKey)

    html = '''\
    <html>
    <head>
        <title>Sub-merchant checkout page</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    </head>
    <body>
        <center>
        <!-- width required mininmum 482px -->
            <iframe  width="482" height="500" scrolling="No" frameborder="0"  id="paymentFrame" src="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction&merchant_id=$mid&encRequest=$encReq&access_code=$xscode">
            </iframe>
        </center>
    
        <script type="text/javascript">
            $(document).ready(function(){
                $('iframe#paymentFrame').load(function() {
                     window.addEventListener('message', function(e) {
                         $("#paymentFrame").css("height",e.data['newHeight']+'px'); 	 
                     }, false);
                 }); 
            });
        </script>
      </body>
    </html>
    '''
    fin = Template(html).safe_substitute(mid=p_merchant_id, encReq=encryption, xscode=accessCode)

    return fin


# Host Server and Port Number should be configured here.

if __name__ == '__main__':
    app.run(port=4300)



