from cosmos_connection import run_query
from build_graph import graph_data

print("Clearing existing graph...")
run_query("g.V().drop()")

print("Inserting nodes...")

inserted = 0
skipped = 0

for node in graph_data["nodes"]:
    email = node.get("email")

    if not email or "@" not in email:
        skipped += 1
        continue

    domain = email.split("@")[-1]
    is_external = str(node["is_external"]).lower()

    q = (
        "g.addV('User')"
        f".property('id','{email}')"
        f".property('email','{email}')"
        f".property('domain','{domain}')"
        f".property('is_external',{is_external})"
        f".property('pk','global')"
    )

    run_query(q)
    inserted += 1

print(f"Nodes inserted: {inserted}")
print(f"Nodes skipped: {skipped}")

print("Inserting edges...")

edge_inserted = 0

for edge in graph_data["edges"]:
    src = edge["from"]
    dst = edge["to"]

    if not src or not dst:
        continue

    q = (
        f"g.V('{src}')"
        ".addE('SENT_TO')"
        f".to(g.V('{dst}'))"
        f".property('count',{edge['count']})"
        f".property('risk',{edge['risk']})"
        f".property('pk','global')"   # REQUIRED
    )

    run_query(q)
    edge_inserted += 1

print(f"Edges inserted: {edge_inserted}")
print("GRAPH PUSH COMPLETE")
