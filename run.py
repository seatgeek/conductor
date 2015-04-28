import adwords_api
import process

from googleads import adwords

adwords_client = adwords.AdWordsClient.LoadFromStorage()
adwords_api.get_campaigns(adwords_client)
for campaign_id, campaign_name in zip(adwords_api.campaign_ids, adwords_api.campaign_names):
    process.run_job(campaign_id, campaign_name)
