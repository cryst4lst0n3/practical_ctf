import onnx

model = onnx.load(r"D:\CTF\practical\Aug-26\ddc26\emotionet\emotionnet_v2.onnx")

print(len(model.graph.node))
for i, node in enumerate(model.graph.node):
    print(i, node.op_type, node.name)