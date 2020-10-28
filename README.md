# rigodenas
Elasticsearch commands:

Delete index: curl -XDELETE http://192.168.0.210:9200/demo
List indices: curl -XGET http://192.168.0.210:9200/_cat/indices?v

Kibana:
http://192.168.0.210:5601/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(columns:!(_source),filters:!(),index:'3e9b8da0-1889-11eb-81d3-43188b9080e8',interval:auto,query:(language:kuery,query:%22jynx%22),sort:!())

NAS command:
/volume1/@appstore/py3k/usr/local/bin/python3 FTPCrawler.py