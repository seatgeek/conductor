import os
import datetime
import time

from googleads import errors


hour = datetime.datetime.now().time().hour

ad_group_id = []
keyword_id = []
keyword_bid = []
campaign_ids = []
campaign_names = []


def get_campaigns(client):
    campaign_service = client.GetService('CampaignService', version='v201409')
    selector = {
        'fields': ['Id', 'Name', 'Status'],
        'predicates': [
            {
                'field': 'Labels',
                'operator': 'CONTAINS_ANY',
                'values': '{LABELID}'
            },
            {
                'field': 'CampaignStatus',
                'operator': 'EQUALS',
                'values': 'ENABLED'
            }
        ]
    }
    page = campaign_service.get(selector)
    for campaign in page['entries']:
        campaign_ids.append(str(campaign['id']))
        campaign_names.append(str(campaign['name']))
    return campaign_ids
    return campaign_names


# This function pulls a report of Campaign cost in the last 14 days by hour in order to compare to hourly revenue later.
def get_report(client, campaign_id):
    report_downloader = client.GetReportDownloader(version='v201409')
    report_name = 'report'
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), report_name + ".csv")
    # Create report definition.
    report = {
        'reportName': 'Hourly Report',
        'dateRangeType': 'LAST_14_DAYS',
        'reportType': 'CAMPAIGN_PERFORMANCE_REPORT',
        'downloadFormat': 'CSV',
        'selector': {
            'fields': ['HourOfDay', 'Cost'],
            'predicates': [
                {
                    'field': 'CampaignId',
                    'operator': 'EQUALS',
                    'values': campaign_id
                }
            ]
        },
        # Enable to get rows with zero impressions.
        'includeZeroImpressions': 'false'
    }

    # You can provide a file object to write the output to. For this demonstration
    # we use sys.stdout to write the report to the screen.
    f = open(path, 'wb')
    f.write(report_downloader.DownloadReportAsString(report, skip_report_header=True, skip_report_summary=True))
    f.close()


# This function pulls a report on the Average CPC over the last 14 days. Unfortunately Adwords API doesn't let you pull
# keyword reports by Hour of Day
def get_keywords(client, campaign_id):
    report_downloader = client.GetReportDownloader(version='v201409')
    report_name = 'keywords'
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), report_name + ".csv")
    # Create report definition.
    report = {
        'reportName': 'Hourly Report',
        'dateRangeType': 'LAST_14_DAYS',
        'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
        'downloadFormat': 'CSV',
        'selector': {
            'fields': ['AdGroupId', 'Id', 'AverageCpc'],
            'predicates': [
                {
                    'field': 'CampaignId',
                    'operator': 'EQUALS',
                    'values': campaign_id
                }
            ]
        },
        # This script only operates on keywords that have seen impressions in the last 14 days
        'includeZeroImpressions': 'false'
    }

    f = open(path, 'wb')
    f.write(report_downloader.DownloadReportAsString(report, skip_report_header=True, skip_report_summary=True))
    f.close()


# This function actually changes the bids on your keywords as the last step
def change_bids(client, ad_group_id, criterion_id, new_bid, length):
    RETRY_INTERVAL = 10
    RETRIES_COUNT = 30
    # Initialize appropriate service.
    mutate_job_service = client.GetService('MutateJobService', version='v201409')

    # Create list of all operations for the job.
    operations = []

    # Create AdGroupCriterionOperations to change keywords.
    for x in range(0, length):
        operations.append({
            'xsi_type': 'AdGroupCriterionOperation',
            'operator': 'SET',
            'operand': {
                'xsi_type': 'BiddableAdGroupCriterion',
                'adGroupId': ad_group_id[x],
                'criterion': {
                    'id': criterion_id[x],
                },
                'biddingStrategyConfiguration': {
                    'bids': [
                        {
                            'xsi_type': 'CpcBid',
                            'bid': {
                                'microAmount': new_bid[x]
                            }
                        }
                    ]
                }
            }
        })

    # You can specify up to 3 job IDs that must successfully complete before
    # this job can be processed.
    policy = {
        'prerequisiteJobIds': []
    }
    # Call mutate to create a new job.

    response = mutate_job_service.mutate(operations, policy)

    if not response:
        raise errors.GoogleAdsError('Failed to submit a job; aborting.')
    job_id = response['id']
    print 'Job with ID %s was successfully created.' % job_id

    # Create selector to retrieve job status and wait for it to complete.
    selector = {
        'xsi_type': 'BulkMutateJobSelector',
        'jobIds': [job_id]
    }

    time.sleep(RETRY_INTERVAL)
    # Poll for job status until it's finished.
    print 'Retrieving job status...'
    for i in range(RETRIES_COUNT):
        job_status_response = mutate_job_service.get(selector)
        status = job_status_response[0]['status']
        if status in ('COMPLETED', 'FAILED'):
            break
        print ('[%d] Current status is \'%s\', waiting %d seconds to retry...' %
               (i, status, RETRY_INTERVAL))
        time.sleep(RETRY_INTERVAL)

    if status == 'FAILED':
        raise errors.GoogleAdsError('Job failed with reason: \'%s\'' %
                                    job_status_response[0]['failure_reason'])
    if status in ('PROCESSING', 'PENDING'):
        raise errors.GoogleAdsError('Job did not complete within %d seconds' %
                                    (RETRY_INTERVAL * (RETRIES_COUNT - 1)))

    # Status must be COMPLETED.
    # Get the job result. Here we re-use the same selector.
    result_response = mutate_job_service.getResult(selector)

    # Output results.
    index = 0
    for result in result_response['SimpleMutateResult']['results']:
        if 'PlaceHolder' in result:
            print 'Operation [%d] - FAILED' % index
        else:
            print 'Operation [%d] - SUCCEEDED' % index
        index += 1


# Uncomment these various lines in order to QA each step.
# if __name__ == '__main__':
    # CAMPAIGN_ID = 'INSERT A CAMPAIGN ID'
    # adwords_client = adwords.AdWordsClient.LoadFromStorage()
    # get_keywords(adwords_client, CAMPAIGN_ID)
    # get_campaigns(adwords_client)
    # get_report(adwords_client, CAMPAIGN_ID)
