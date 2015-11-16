from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

# creating the network
n = FeedForwardNetwork()

# creating the layers
inLayer = LinearLayer(2)
hiddenLayer = SigmoidLayer(3)
outLayer = LinearLayer(1)

# adding the layer to the network
n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)

# creating the connections (full network in this example)
in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)

# adding the connections to the netwokr
n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)


# initialization