import json
json_obj = json.loads("deals.txt")

deal_details = json_obj['dealDetails']

for key in deal_details:
	deal = deal_details[key]
	if (deal['impressionAsin'] != deal['teaserAsin']):
		print deal['impressionAsin'], deal['teaserAsin']