import adwords_api
import create_bids
import db_connect

from googleads import adwords


def run_job(campaign_id, campaign_name):
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    new_bids = []
    db_connect.get_transactions(campaign_id)
    print "Retrived Transactions for Campaign " + campaign_name
    adwords_api.get_report(adwords_client, campaign_id)
    print "Retrived Adwords Spend for Campaign " + campaign_name
    adwords_api.get_keywords(adwords_client, campaign_id)
    print "Retrived Keywords for Campaign " + campaign_name
    create_bids.multipliers()
    print "Created Bid Multipliers for Campaign " + campaign_name
    create_bids.batch_parameters()
    for cpc in create_bids.keyword_cpc:
        l = round((int(cpc)*create_bids.multiple[0]), -4)
        new_bids.append(int(l))
    create_bids.multiple = []
    print "Created New Bids for Campaign " + campaign_name
    length = len(new_bids)
    print "Sending New Bids to Adwords for Campaign " + campaign_name
    adwords_api.change_bids(adwords_client, create_bids.ad_group_id, create_bids.keyword_id, new_bids, length)
    print "All Done on Campaign " + campaign_name
