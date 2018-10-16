import copy


number_of_nodes = 0

subvols= []
total_size_per_node = 100
prev_volume_size = 0


def initial_nodes(num):
    global number_of_nodes
    number_of_nodes = num


def volume_size():
    nodes = get_nodes()

    volsize = 0
    for sv in subvols:
        b1_size = total_size_per_node / len(nodes[sv[0]["node"]])
        b2_size = total_size_per_node / len(nodes[sv[1]["node"]])
        b3_size = total_size_per_node / len(nodes[sv[2]["node"]])
        volsize += min(b1_size, b2_size, b3_size)

    return int(volsize)


def add_subvol():
    subvols.append([])


def add_brick(subvol_idx, brick):
    global subvols
    brick["subvol"] = subvol_idx
    subvols[subvol_idx].append(brick)


def add_node():
    global number_of_nodes
    number_of_nodes += 1


def replace_brick(src_node, dest_node, svid, brickname):
    global subvols
    for idx, b in enumerate(subvols[svid]):
        if b["name"] == brickname:
            subvols[svid][idx]["node"] = dest_node


def get_nodes():
    nodes = [[] for _ in range(number_of_nodes)]
    for svidx, bricks in enumerate(subvols):
        for b in bricks:
            nodes[b["node"]].append(copy.copy(b))
    return nodes


def show_bricks_summary():
    global prev_volume_size

    print()
    volsize = volume_size()
    pchange = ""
    if prev_volume_size > 0:
        pchange = " Growth=+%s%%" % int((volsize-prev_volume_size)*100/prev_volume_size)
        pchange = pchange.ljust(13)

    nodes = get_nodes()
    max_size = int((len(nodes) * total_size_per_node)/3)
    message = ""
    if prev_volume_size > 0:
        utilization_msg = "Utilization=%s%%" % (int(volsize*100/max_size))
        utilization_msg = utilization_msg.ljust(16)
        message = " %s Max size possible=%sG" % (utilization_msg, max_size)
    else:
        message = " Growth=--    Utilization=100%% Max size possible=%sG" % max_size

    print(".**Volume Size=%sG%s%s Number of Nodes=%s**" % (volsize, pchange, message, number_of_nodes))
    prev_volume_size = volsize
            
    max_bricks_per_node = 0
    header = ""
    underline = ""
    for nidx, ndata in enumerate(nodes):
        headerstr = "Node %s" % (nidx+1)
        header += headerstr.ljust(15) + " "
        underline += "".ljust(15, "-")

        if max_bricks_per_node < len(ndata):
            max_bricks_per_node = len(ndata)

    print("----")
    print(header)
    print(underline)
    for row in range(0, max_bricks_per_node):
        out = ""
        for ndata in nodes:
            if len(ndata) >= row + 1:
                outstr = "%s:%s" % (ndata[row]["subvol"]+1, ndata[row]["name"])
                out += outstr.ljust(15) + " "
            else:
                out += "".ljust(15) + " "

        print(out)

    print("----")


def main():
    initial_nodes(3)
    bricks_per_node = 8

    # Initial Volume creation with 8 sub volumes
    for sv in range(0, 8):
        add_subvol()

        add_brick(sv, {
            "node": 0,
            "name": "brick%d" % (sv*3 + 1)
        })

        add_brick(sv, {
            "node": 1,
            "name": "brick%d" % (sv*3 + 2)
        })

        add_brick(sv, {
            "node": 2,
            "name": "brick%d" % (sv*3 + 3)
        })

    # Show bricks layout
    show_bricks_summary()

    for i in range(21):
        add_node()
        nodes = get_nodes()
        nodes = sorted(nodes, key=len, reverse=True)

        max_bricks_count = 0
        for n in nodes:
            if len(n) > max_bricks_count:
                max_bricks_count = len(n)

        new_bricks_per_node = int(24/(number_of_nodes))

        nreplaced = 0
        subvol_in_new_node = []
        while nreplaced < new_bricks_per_node:
            for nidx, bricks in enumerate(nodes):
                if nreplaced >= new_bricks_per_node:
                    break

                if len(bricks) <= new_bricks_per_node:
                    continue

                remaining_bricks = len(bricks)
                for b in bricks:
                    if nreplaced >= new_bricks_per_node:
                        break

                    if remaining_bricks <= new_bricks_per_node:
                        break

                    if b["subvol"] not in subvol_in_new_node:
                        subvol_in_new_node.append(b["subvol"])
                        replace_brick(b["node"], number_of_nodes-1, b["subvol"], b["name"])
                        nreplaced += 1
                        remaining_bricks -= 1
                        break

        show_bricks_summary()
        bricks_per_node = new_bricks_per_node


if __name__ == "__main__":
    main()
