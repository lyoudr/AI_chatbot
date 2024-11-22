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

# Gossip Protocol
# is peer-to-peer communication mechanism that 
# allows nodes to exchange state information about each other.
# This protocol helps nodes stay informed about the state of the cluster
# including which nodes are active, failed or temporarily unreachable.

# Mechanism: Each node "gossips" with a subset of other
# nodes periodically, sharing information about itself and other nodes it knows about.
# This data propagates through the cluster, so each node eventually has a nearly complete
# view of the system

# 2. Tunalbe Consistency
# ONE: Only one replica node needs to acknowledge the read or write, providing the lowest latency but weakest 
# QUORUM: A majority (quorum) of replica nodes must acknowledge the read or write, balancing consistency with 