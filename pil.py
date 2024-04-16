from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from premailer import transform
import base64
from email.mime.image import MIMEImage
from ccavutil import encrypt, decrypt
import json
import random
from datetime import datetime, timedelta
from string import Template
import threading
import razorpay
import requests

def razorpay_client_credentials(studio):
    if studio in ["NDA","SD","IPM","GGN"]:
        razorpay_key_id = 'rzp_live_mxqGmvv7wvDwCM'
        razorpay_key_secret = '5Y7eDdJE819LCsBIiiZzgavQ'

    else:
        razorpay_key_id = 'rzp_live_Nl7U5V8xK8TXSI'
        razorpay_key_secret = '52nqEc0i23t8nTrtbjpppeSW'

    return {"id": razorpay_key_id, "secret": razorpay_key_secret}

@app.route('/landing-page')
def landing_page_dropin():
    session_id = os.urandom(16).hex()
    return render_template("landingpage.html", session_id=session_id, fee=640, event='landingpage')


@app.route('/payment-method-landingpage/<session_id>/<int:fee>/<event>', methods=['GET', 'POST'])
def make_payment_pinkd(session_id, fee, event):
    # Get the selected batches as a
    # session_id = request.form.get('session_id')
    print(request.form.get('dob'))
    if fee == "":
        flash('Please Select a date and Batch!', 'error')
        return redirect(url_for('registration_form_dropin'))
    else:

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        dob = request.form['dob']
        studio = 'ED'
        print()

        today_date = datetime.today().strftime('%d-%b-%Y %H:%M:%S')
        dropin_studio = session.get('studio')
        if session_id not in user_data:
            user_data[session_id] = {
                'name': None,
                'phone': None,
                'email': None,
                'studio': None

            }

        user_data[session_id]['name'] = name
        user_data[session_id]['phone'] = phone
        user_data[session_id]['email'] = email
        user_data[session_id]['studio'] = studio

        print(user_data)

        sheet = client.open_by_key(sheet_key).worksheet("Payment_Incomplete(Pinkd)")
        dropin_data = [dob, name, phone, email, studio]

        sheet.append_row(dropin_data)





        session['batches'] = event
        session['order_amount'] = fee * 100  # Convert fee to the smallest currency unit (in paisa)
        order_amount = session.get('order_amount')
        print(order_amount)
        print('YESS')

        # Create a new order in Razorpay

        order_data = {
                'amount': order_amount,
                'currency': 'INR',
                # 'receipt': order_receipt,
                'payment_capture': 1,  # Auto-capture the payment

                    # Add any other parameters as required
                }
        razorpay_client = razorpay.Client(auth=(razorpay_client_credentials(user_data[session_id]['studio'])['id'], razorpay_client_credentials(user_data[session_id]['studio'])['secret']))
        user_data[session_id]['razorpay_key'] = razorpay_client_credentials(user_data[session_id]['studio'])['id']
        session['order_response'] = razorpay_client.order.create(data=order_data)
        session['fee'] = round(order_amount/100 * 1.18)

        order_response = session.get('order_response')
        fee = fee

        print(fee)



        if order_response.get('id'):
            session['order_id'] = order_response['id']
            session['batches'] = ""
            session['fee_without_gst'] = fee
            session['fee_with_gst'] = str(round(float(session.get('fee_without_gst')) * 1.18))


            session['validity'] = event

            order_id = session.get('order_id')
            batches = session.get('batches')
            fee_without_gst = session.get('fee_without_gst')
            fee_with_gst = session.get('fee')

            session['internet_handling_fees'] = round((float(fee_with_gst) / 0.9764 * 100) * 0.0236 / 100, 2)
            session['fee_final'] = round(int(float(fee_with_gst) / 0.9764 * 100))
            session['gst'] = round(float(fee_without_gst) * 0.18,2)

            gst = session.get('gst')
            internet_handling_fees = session.get('internet_handling_fees')
            fee_final = session.get('fee_final')

            validity = session.get('validity')
            paid_to = "Pink Grid"



            user_data[session_id]['order_receipt'] = ""
            user_data[session_id]['batch'] = batches
            user_data[session_id]['validity'] = validity
            user_data[session_id]['razorpay_id'] = order_response['id']
            user_data[session_id]['fee_without_gst'] = fee_without_gst
            user_data[session_id]['fee_with_gst'] = fee_with_gst
            user_data[session_id]['gst'] = gst
            user_data[session_id]['internet_handling_fees'] = internet_handling_fees
            user_data[session_id]['fee_final'] = fee_final/100

            print(user_data)
            print(session_id)
            print(f"razorpay keyyyy {user_data[session_id]['razorpay_key']}")

            print(session)
            # Redirect the user to the Razorpay payment page
            return render_template("pay.html", payment=order_response,
                                   fee_without_gst=float(fee_without_gst),
                                   gst=gst, internet_handling_fees=internet_handling_fees, fee_final=fee_final,razorpay_key=user_data[session_id]['razorpay_key'], session_id=session_id)

        else:
            # Failed to create the order
            return render_template('failed.html')
