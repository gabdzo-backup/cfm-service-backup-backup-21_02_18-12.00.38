# cfm-service
Service for cook for me app.

## Running with C* backend

* The `bin/cfm-service` script is configured to start the service using Cassandra backend.
* To make this work, you need to:
  * In `cfm_service/cassandra_settings` fill in the username and password.
  * Place the `secure-connect-cfm.zip` into the root of the repo.
  * Run `./bin/cfm-service`.
  * You should see:
  ```text
  2020-09-30 16:09:29,024 INFO cfm_service.server MainThread : Storage backend will be: cassandra
  2020-09-30 16:09:29,024 DEBUG root MainThread : Looking for recipes from root folder /Users/zvo/cfm/cfm-service/cfm_cms/cms/en-us
  2020-09-30 16:09:29,980 INFO cassandra.policies MainThread : Using datacenter 'dc-1' for DCAwareRoundRobinPolicy (via host 'd5fe239e-b6c5-44e1-b0b1-7082414c2a78-europe-west1.db.astra.datastax.com:31099:f50e75b6-514a-4b7c-9f01-bce64e73da74'); if incorrect, please specify a local_dc to the constructor, or limit contact points to local cluster nodes
  2020-09-30 16:09:31,733 WARNING cassandra.cluster event_loop : Host d5fe239e-b6c5-44e1-b0b1-7082414c2a78-europe-west1.db.astra.datastax.com:31099:f50e75b6-514a-4b7c-9f01-bce64e73da74 error: Server error.
  2020-09-30 16:09:31,836 INFO werkzeug MainThread :  * Running on http://127.0.0.1:5252/ (Press CTRL+C to quit)
  ```
* The cassandra_storage saves a sample pantry under id `-1`:
  ```text
  cfm_db_admin@cqlsh> select * from cfm.pantry;
  
   pantry_id | blob
  -----------+-------------
          -1 | egg,1,piece
  
  (1 rows)    
  ```
* In another terminal, run:
  ```text
  curl -v http://127.0.0.1:5252/advice/-1
  ``` 
  * This should go through and you should get some advice.