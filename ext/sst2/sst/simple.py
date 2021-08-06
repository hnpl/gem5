import sst
import sys
import os

cache_link_latency = "1ns"

l1_params = {
    "access_latency_cycles" : "1",
    "cache_frequency" : "2 Ghz",
    "replacement_policy" : "lru",
    "coherence_protocol" : "MESI",
    "associativity" : "4",
    "cache_line_size" : "64",
    "cache_size" : "4 KB",
    "L1" : "1",
    "debug" : "0",
}

l2_params = {
    "access_latency_cycles" : "8",
    "cache_frequency" : "2 Ghz",
    "replacement_policy" : "lru",
    "coherence_protocol" : "MESI",
    "associativity" : "8",
    "cache_line_size" : "64",
    "cache_size" : "32 KB",
    "debug" : "0",
}

cpu_params = {
    "frequency": "3GHz",
    "cmd": "gem5/riscv_fs.py"
}

gem5_node = sst.Component("node", "gem5.gem5Component")
gem5_node.addParams(cpu_params)

system_port = gem5_node.setSubComponent("system_port", "gem5.gem5Bridge", 0)
cache_port = gem5_node.setSubComponent("cache_port", "gem5.gem5Bridge", 0)

"""
# L1 icache
l1i_cache = sst.Component("l1i_cache", "memHierarchy.Cache")
l1i_cache.addParams(l1_params)
# L1 dcache
l1d_cache = sst.Component("l1d_cache", "memHierarchy.Cache")
l1d_cache.addParams(l1_params)
"""

# L1 cache
l1_cache = sst.Component("l1_cache", "memHierarchy.Cache")
l1_cache.addParams(l1_params)

# TODO: shared L2Cache

# Memory
memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
    "debug" : "0",
    "clock" : "1GHz",
    "request_width" : "64",
    "addr_range_end" : 1024*1024*1024-1,
})
memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "access_time" : "30ns",
    "mem_size" : "4GiB",
})


# Connections
# cpu <-> L1
"""
cpu_icache_link = sst.Link("cpu_l1i_cache_link")
cpu_icache_link.connect(
    (gem5_node, "icache_port", cache_link_latency),
    (l1i_cache, "high_network_0", cache_link_latency)
)

cpu_dcache_link = sst.Link("cpu_l1d_cache_link")
cpu_dcache_link.connect(
    (gem5_node, "dcache_port", cache_link_latency),
    (l1d_cache, "high_network_0", cache_link_latency)
)
"""

cpu_cache_link = sst.Link("cpu_l1_cache_link")
cpu_cache_link.connect(
    (cache_port, "port", cache_link_latency),
    (l1_cache, "high_network_0", cache_link_latency)
)

# L1 <-> mem
"""
icache_mem_link = sst.Link("l1i_cache_mem_link")
icache_mem_link.connect(
    (l1i_cache, "low_network_0", cache_link_latency),
    (memctrl, "direct_link", cache_link_latency)
)
dcache_mem_link = sst.Link("l1d_cache_mem_link")
dcache_mem_link.connect(
    (l1d_cache, "low_network_0", cache_link_latency),
    (memctrl, "direct_link", cache_link_latency)
)
"""
cache_mem_link = sst.Link("l1_cache_mem_link")
cache_mem_link.connect(
    (l1_cache, "low_network_0", cache_link_latency),
    (memctrl, "direct_link", cache_link_latency)
)
