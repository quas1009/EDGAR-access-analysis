spark-submit --master spark://$SPARK_CLUSTER:7077 \
             --packages org.apache.spark:spark-streaming-kafka-0-10_2.11:2.4.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 \
             --jars $PWD/postgresql-42.2.9.jar \
             --driver-memory 4G \
             --executor-memory 4G \
             streaming/stream.py