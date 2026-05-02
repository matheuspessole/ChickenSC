(function(sys, proc, ram, tech)
    local log_table = {
        "╔════════════════════════════════════════╗\n",
        "║           ChickenSC - DIAGNOSTIC       ║\n",
        "╚════════════════════════════════════════╝\n\n",
        "> System: " .. sys .. "\n",
        "> Processor: ".. proc.. "\n",
        "> RAM: " .. ram .."\n",
        "> Architecture: " .. tech .."\n\n",
        "══════════════════════════════════════════\n"
    }
    return table.concat(log_table)
end)
