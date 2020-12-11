import grass.script as gscript

buffer = [250,500,1000,2500,5000]
for i in buffer:
    gscript.run_command('r.buffer',
        input = "motorways_raster",
        output = "motorways_buffer" + str(i),
        distances = i)
    gscript.run_command("r.stats.zonal",
        flags = "r",
        base = "motorways_buffer" + str(i),
        cover = "global_human_settlement_data",
        method = "sum",
        output = "population_buffer" + str(i))
    gscript.run_command("r.stats",
        flags = "cln",
        input = "population_buffer" + str(i),
        separator = "tab")