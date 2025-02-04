# from diagrams import Cluster, Diagram, Edge
# from diagrams.gcp.analytics import PubSub
# from diagrams.gcp.compute import AppEngine
# from diagrams.gcp.iot import IotCore

# with Diagram("Message Collecting", show=True, filename="test", direction="TB", edge_attr={"splines": "curved"}) as dg:
#     # pubsub = PubSub("pubsub")

#     # with Cluster("Source of Data"):
#     #     [IotCore("core1"), IotCore("core2"), IotCore("core3")] >> pubsub

#     # with Cluster("Targets"):
#     #     with Cluster("Data Flow"):
#     #         flow = Dataflow("data flow")

#     #     with Cluster("Data Lake"):
#     #         flow >> [BigQuery("bq"), GCS("storage")]

#     #     with Cluster("Event Driven"):
#     #         with Cluster("Processing"):
#     #             flow >> AppEngine("engine") >> BigTable("bigtable")

#     #         with Cluster("Serverless"):
#     #             flow >> Functions("func") >> AppEngine("appengine")

#     # pubsub >> flow
#     csw1 = PubSub("csw01")
#     csw2 = PubSub("csw02")
#     c1 = Edge(label="g0/47-g0/48", style="minlen=5;color=blue")
#     c2 = Edge(label="g0/48-g0/47")
#     c3 = Edge(label="g0/46-g0/46")
#     c4 = Edge(label="g0/1-g0/44",)
#     c5 = Edge(label="g0/2-g1/44", )
#     c6 = Edge(label="g0/1-g0/43")
#     c7 = Edge(label="g0/2-g1/43")
#     with Cluster("WCL"):
#         wac1 = IotCore("wac01")
#         wac2 = IotCore("wac02")
#     with Cluster("ServerRoom 1"):
#         asw1 = AppEngine("asw01")
#         asw2 = AppEngine("asw02")
#         asw3 = AppEngine("asw03")
#     with Cluster("ServerRoom 4"):
#         asw4 = AppEngine("asw04")
#         asw5 = AppEngine("asw05")
#         asw6 = AppEngine("asw06")
#         asw7 = AppEngine("asw07")
#     c8 = Edge(label="g0/3-g0/47")
#     c9 = Edge(label="g0/4-g0/48")
#     c10 = Edge(label="g0/3-g0/48")
#     c11 = Edge(label="g0/4-g0/48")

#     c12 = Edge(label="g0/3-g0/47", )
#     c13 = Edge(label="g0/4-g0/48")
#     c14 = Edge(label="g0/3-g0/48")
#     c15 = Edge(label="g0/4-g0/48")

#     c16 = Edge(label="g0/3-g0/47", )
#     c17 = Edge(label="g0/4-g0/48")
#     c18 = Edge(label="g0/3-g0/48")
#     c19 = Edge(label="g0/4-g0/48")
#     c20 = Edge(label="g0/3-g0/47", )
#     c21 = Edge(label="g0/4-g0/48")
#     c22 = Edge(label="g0/3-g0/48")
#     c23= Edge(label="g0/4-g0/48")

#     csw1 >>c1 >> csw2
#     csw1 >>c2>> csw2
#     csw1 >>c3>> csw2
#     wac1 >> c4 >> csw1
#     wac1 >> c5 >> csw1
#     csw2 >> c6 >> wac2
#     csw2 >> c7 >>  wac2
#     csw1 >> c8 >> asw1
#     csw2 >> c9 >> asw1
#     csw1 >> c10 >> asw2
#     csw2 >> c11 >> asw2
#     csw1 >> c12 >> asw3
#     csw2 >> c13 >> asw3
#     csw1 >> c14 >> asw4
#     csw2 >> c15 >> asw4
#     csw1 >> c16 >> asw5
#     csw2 >> c17 >> asw5
#     csw1 >> c18 >> asw6
#     csw2 >> c19 >> asw6
#     csw1 >> c20 >> asw7
#     csw2 >> c21 >> asw7

    

