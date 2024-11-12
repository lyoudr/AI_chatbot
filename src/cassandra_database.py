from cassandra.cluster import Cluster 
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement

# Define Cassandra cluster connection and session
def get_cassandra_session():
    # Configuration for Cassandra connection (update with your settings)
    cassandra_host = 'localhost'
    cassandra_port = 9042
    cassandra_keyspace = 'ann'

    # Initialize cluster and session
    cluster = Cluster([cassandra_host], port = cassandra_port)
    session = cluster.connect(cassandra_keyspace)

    return session