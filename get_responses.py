from jshelper import create_payment, execute_payment, get_payment_status
import re


def get_response(conversation_history, user_id, user_message):
    N = len(conversation_history[user_id])
    msg = user_message.lower()
    message_len = len(msg)
    match = re.search(r"-?\d+(\.\d+)?", msg)

    if message_len > 50:
        return 'Please keep your messages under 50 characters. Thank you!'

    elif msg.startswith('yes') and N<=0:
        conversation_history[user_id].append(user_message)
        return 'Great! Can you provide the email address associated with the Paypal account you want to send the payment to?'

    elif '@' in msg and N>0:
        split_message = msg.split(' ')
        for sub_message in split_message:
            if '@' in sub_message:
                conversation_history[user_id].append(sub_message)
                break

        return 'Thank you! How much would you like to send to this account?'

    elif match and N>0:
        amount = match.group()
        if float(amount)<=0.0:
            return 'Please enter an amount greater than 0.'

        email_address = conversation_history[user_id][-1]
        confirm_message = 'send '+amount+' dollars to the account owner of '+email_address
        conversation_history[user_id].append(amount)
        return 'Cool! Please confirm that you want to '+confirm_message+". Can I proceed with the transaction?"

    elif 'yes' in msg and N>0:
        amount = conversation_history[user_id][-1]
        payee_email = conversation_history[user_id][N-2]
        payment_response = create_payment(amount, payee_email)
        conversation_history[user_id].append(payment_response['id'])
        approval_url = next(
            link["href"] for link in payment_response["links"] if link["rel"] == "approval_url"
        )
        return "Transaction initiated successfully! Please approve it at "+approval_url+". Respond with 'approved' once you have approved the payment."
    elif 'approved' in msg and N>0:
        payment_id = conversation_history[user_id][-1]
        payment_status = get_payment_status(payment_id)
        if 'payer' not in payment_status:
            return "Payment not approved. Please approve the payment and try again."
        payer_id = payment_status['payer']['payer_info']['payer_id']
        execute_payment(payer_id, payment_id)
        return 'Thank you! Your payment was successful. Please check your Paypal balance. Have a good day!'
    elif N>0:
        conversation_history[user_id].clear()
        return "I'm sorry. Please start the transaction process again."

    return 'None'