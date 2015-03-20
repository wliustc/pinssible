<?php

$content = file_get_contents("deals.txt");

$objs = json_decode($content, true);

if (!$objs){
	echo "Invalid json file";
	exit();

}

$deals = $objs['dealDetails'];
#var_dump($deals);
foreach ($deals as $key=>$deal){
	#$deal = $deals[$key];
	#var_dump($deal);

	if ($deal['impressionAsin'] != $deal['teaserAsin']) {
		echo $deal['impressionAsin'], "\n";
	}
}

$url = "http://www.amazon.com/xa/dealcontent/v2/GetDealStatus?nocache=1426213473087";

echo file_get_contents($url);