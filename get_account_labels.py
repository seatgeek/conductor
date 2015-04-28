from googleads import adwords

campaign_ids = []
campaign_names = []
campaign_labels = []


def get_campaigns(client):
    campaign_service = client.GetService('CampaignService', version='v201409')
    selector = {
        'fields': ['Id', 'Name', 'Status', 'Labels'],
        'predicates': [
            {
                'field': 'CampaignStatus',
                'operator': 'EQUALS',
                'values': 'ENABLED'
            }
        ]
    }
    page = campaign_service.get(selector)
    print page

if __name__ == '__main__':
    # Initialize client object.
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    get_campaigns(adwords_client)
