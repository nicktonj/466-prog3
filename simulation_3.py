'''
Created on Oct 12, 2016

@author: mwittie
'''
import network_3 as network
import link_3 as link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 20 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    # Router Tables
    table_A = {
        1: 0,
        2: 1
    }
    table_B = {
        1: 0
    }
    table_C = {
        2: 0
    }
    table_D = {
        1: 0,
        2: 1
    }

    
    object_L = [] #keeps track of objects, so we can kill their threads
    
    #create network nodes
    # Host 1
    client1 = network.Host(1)
    object_L.append(client1)

    # Host 2
    client2 = network.Host(2)
    object_L.append(client2)

    # Host 3
    server1 = network.Host(3)
    object_L.append(server1)

    # Host 4
    server2 = network.Host(4)
    object_L.append(server2)

    # Router A
    router_a = network.Router(name='A', intf_count=len(table_A), max_queue_size=router_queue_size, routing_table=table_A)
    object_L.append(router_a)

    # Router B
    router_b = network.Router(name='B', intf_count=len(table_B), max_queue_size=router_queue_size, routing_table=table_B)
    object_L.append(router_b)

    # Router C
    router_c = network.Router(name='C', intf_count=len(table_C), max_queue_size=router_queue_size, routing_table=table_C)
    object_L.append(router_c)

    # Router D
    router_d = network.Router(name='D', intf_count=len(table_D), max_queue_size=router_queue_size, routing_table=table_D)
    object_L.append(router_d)
    
    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    link_layer.add_link(link.Link(client1, 0, router_a, 0, 50))
    link_layer.add_link(link.Link(client2, 0, router_a, 1, 50))

    # Router A links to next object
    link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))
    link_layer.add_link(link.Link(router_a, 1, router_c, 0, 50))

    # Router B links to next object
    link_layer.add_link(link.Link(router_b, 0, router_d, 0, 30))

    # Router C links to next object
    link_layer.add_link(link.Link(router_c, 0, router_d, 1, 30))

    # Router D links to next object
    link_layer.add_link(link.Link(router_d, 0, server1, 0, 50))
    link_layer.add_link(link.Link(router_d, 1, server2, 0, 50))
    
    
    #start all the objects
    thread_L = []

    # Host Threads
    thread_L.append(threading.Thread(name=client1.__str__(), target=client1.run))
    thread_L.append(threading.Thread(name=client2.__str__(), target=client2.run))
    thread_L.append(threading.Thread(name=server1.__str__(), target=server1.run))
    thread_L.append(threading.Thread(name=server2.__str__(), target=server2.run))

    # Routerr Threads
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()
    
    
    #create some send events    
    for i in range(3):
        message = 'Sample data yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaay %d' % i
        client1.udt_send(1, 3, message)
        client2.udt_send(2, 4, message)
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically
