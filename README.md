Conductor is a script that uses data from your internal database in order to build out hourly bid modifiers for your Adwords campaigns.

### What can Conductor do?

* Modify bids at the keyword level for all tagged campaigns based on time of day performance
* Pull information from your database in order to calculate bid modifiers
* Work off a CPA or ROI target

### What can't Conductor do?

* Modifiy bids based on individual adgroup or keyword level performance
* Modify bids based on time of day _and_ day of week

### How do I set Conductor up?

1. Get adwords API access [here](https://developers.google.com/adwords/api/docs/signingup)
2. Set up [labels](https://support.google.com/adwords/answer/2475865?hl=en) for campaigns you'd like this script to operate on.
3. Clone this repo down to your computer. If you've never done that before, follow the instructions [here](https://help.github.com/articles/fetching-a-remote/#clone)
4. Follow the instructions [here](https://developers.google.com/adwords/api/docs/first-request) for finding all necessary credentials.
6. Set up database credentials [here](https://github.com/seatgeek/adwords-hourly-bid-updater/blob/master/db_connect.py) and the query that either gets you revenue for an ROI calculation, or a count of KPIs for a CPA calculation.
 * This file is set up for a Postgres based DB. If you work off of a MySQL DB then you'll need to follow the instructions found [here](http://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html) for accessing your DB.
5. Add your `CLIENT_ID` and `CLIENT_SECRET` to `generate_refresh_token.py` then run the command `python generate_refresh_token.py` in the command line. Follow the instructions in order to get your refresh token.
6. Add your `developer_token`, `client_id`, `client_secret`, `client_customer_id`, and `refresh_token` to the file `googleads.yaml`. Copy that file to your home directory.
7. If you are going to use a label to decide which campaigns to run this on, then you must run the following command `python get_account_labels.py`. You will see an output of all campaigns with their attached labels. Copy the `LabelId` for your desired label.
  * If you would instead prefer to run this script on every campaign in your account. You must remove lines 29 - 33 in the `adwords_api.py` file found [here](https://github.com/seatgeek/adwords-hourly-bid-updater/blob/master/adwords_api.py#LL29-33)
8. Paste the `LabelId` into [this](https://github.com/seatgeek/adwords-hourly-bid-updater/blob/master/adwords_api.py#LL32) line in the file `adwords_api.py`
9. Set up your ROI or CPA goal in `create_bids.py` found [here](https://github.com/seatgeek/adwords-hourly-bid-updater/blob/master/create_bids.py)
9. Run this command: `python run.py`. You should see the script operating on all desired campaigns!

### How do I automate this script to run every hour?

You can always ask super nicely to get some help deploying the app to [the cloud](https://www.google.com/search?q=the+cloud&tbm=isch) from your trusty development team...or figure it out yourself!

I haven't taken the time to do this yet, and plan to do more work on this in the future anyway. In the meantime I have it set up to run automatically every hour on my work comp. If your work comp doesn't live at work...this solution may be a problem.

If you've never played around with Applescripts, they are a great way to automate running files on your OSX machine. [This](http://macosxautomation.com/applescript/firsttutorial/index.html) is a pretty good tutorial on Applescripts.

Anyway, just open up Applescripts and paste the content of `automater.apple_script` found [here](https://github.com/seatgeek/adwords-hourly-bid-updater/blob/master/automater.apple_script) into the editor. Make sure you edit line 3 to include the path to the repo.

Save the script as an application.

You can use Apple Calendar's "Alert" [feature](https://discussions.apple.com/docs/DOC-4082) in order to open a file...which in this case will be the application you just created. Set the file to run every hour on the hour and you're good to go.


#### Work at SeatGeek

If this is how you like to solve problems you run into every day at work, then I think you'd get along great with our team. We're hiring for almost everything! Check out our [Jobs Page](https://seatgeek.com/jobs)
