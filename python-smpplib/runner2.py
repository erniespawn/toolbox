import argparse
import datetime
from datetime import datetime, timedelta, date
import gzip
import logging
import smpplib.gsm
import smpplib.client
import smpplib.consts
import sys

parse = argparse.ArgumentParser()
parse.add_argument("s", help='SystemID')
parse.add_argument("s_id", help='SenderID')
parse.add_argument('sc', help='Service Center')
parse.add_argument("msisdn", help='MsIsdn')
parse.add_argument("concat", help='Concat')
parse.add_argument('textSM', help='TextMessage')
args = parse.parse_args()

print (args.s)
print (args.s_id)
print (args.sc)
print (args.msisdn)
print (args.sc)
print (args.concat)
print (args.textSM)



# if you want to know what's happening
logging.basicConfig(level='DEBUG')

# Two parts, UCS2, SMS with UDH
# parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'n django, is there a way to\n'*10)
parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'{}'.format(args.textSM))

client = smpplib.client.Client('smsc-tip-1-eu4-prod', 12776, allow_unknown_opt_params=True)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(
    lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))

client.connect()
# client.bind_transceiver(system_id='{}'.format(args.s), password='ss7s7ack')
# client.bind_transceiver(system_id='{}'.format(args.s), password='ss7s7ack')
client.bind_transceiver(system_id='bics01', password='ss7s7ack')

run_once = "{}".format(args.concat)

for part in parts:
    try:
        while 1:
            if run_once == '1':
                # print ("only sent 1")
                pdu = client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure it is a byte string, not unicode:
                    source_addr='{}'.format(args.s_id),
                    # source_addr='1008',

                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure thease two params are byte strings, not unicode:
                    # destination_addr='',
                    destination_addr='{}'.format(args.msisdn),
                    # destination_addr='6584684667',
                    short_message=part,

                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                    # user_message_reference='3197015001050',
                    user_message_reference='{}'.format(args.sc),
                )
                print(pdu.sequence)

                run_once = 2
                break
            elif run_once == '0':
                # print ("Send both SMS")
                pdu = client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure it is a byte string, not unicode:
                    source_addr='{}'.format(args.s_id),
                    # source_addr='1008',

                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure thease two params are byte strings, not unicode:
                    # destination_addr='',
                    destination_addr='{}'.format(args.msisdn),
                    # destination_addr='6591016186',
                    short_message=part,

                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                    # user_message_reference='3197015001050',
                    user_message_reference='{}'.format(args.sc),
                )
                print(pdu.sequence)

                break
            else:
                print ("Dont run anything")
                break


    except:
        pass


# Enters a loop, waiting for incoming PDUs
client.listen()
